import datetime
import json
from pydoc import pager
from typing import List
from flask_login import current_user
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import select, func, except_
from app.extensions import db, paginate
from app.forms import InterfaceTestcaseFrom
from app.schema import TestCase, TestResultItem, TestResult
import requests


class TestCaseServices:
    # -------------------------------------- 数据库获取数据 -------------------------------------- #
    @staticmethod
    def get_all_case() -> List[TestCase]:
        """获取所有测试用例"""
        return db.session.scalars(select(TestCase)).all()

    @staticmethod
    def get_case_by_interface_id(interface_id: int) -> List[TestCase]:
        """通过接口ID获取用例"""
        return db.session.scalars(
            select(TestCase)
            .where(TestCase.belong_interface_id == interface_id)
        ).all()

    @staticmethod
    def get_case_by_interface_id_page(interface_id: int, page: int):
        """通过接口ID获取用例"""
        return paginate(select(TestCase)
                        .where(TestCase.belong_interface_id == interface_id), page=page)

    @staticmethod
    def get_case_by_interface_list(interface_list: List[int]) -> List[TestCase]:
        """通过多个接口ID获取用例"""
        return db.session.scalars(
            select(TestCase)
            .where(TestCase.belong_interface_id.in_(interface_list))
        ).all()

    @staticmethod
    def get_case_by_id(case_id: int) -> TestCase:
        """通过ID获取单个用例"""
        return db.session.scalar(select(TestCase).where(TestCase.id == case_id))

    @staticmethod
    def get_case_by_case_id_list(case_id_list: List[int]) -> List[TestCase]:
        """通过多个ID获取用例"""
        return db.session.scalars(
            select(TestCase)
            .where(TestCase.id.in_(case_id_list))
        ).all()

    # -------------------------------------- 增删改查操作 -------------------------------------- #

    @staticmethod
    def add_case(form: InterfaceTestcaseFrom) -> TestCase:
        new_case = TestCase(
            testcase_name=form.testcase_name.data,
            headers=form.headers.data,
            params=form.params.data,
            expected_results=form.expected_results.data,
            description=form.description.data,
            belong_interface_id=form.belong_interface.data,
            create_user_id=current_user.id
        )
        db.session.add(new_case)
        db.session.commit()
        return new_case

    @staticmethod
    def edit_case(case_id, form: InterfaceTestcaseFrom) -> TestCase:
        case = TestCaseServices.get_case_by_id(case_id)
        case.testcase_name = form.testcase_name.data
        case.params = form.params.data
        case.headers = form.headers.data
        case.expected_results = form.expected_results.data
        case.description = form.description.data
        case.belong_interface_id = form.belong_interface.data
        case.create_user_id = current_user.id
        db.session.commit()
        return case

    @staticmethod
    def del_case(case_id):
        case = TestCaseServices.get_case_by_id(case_id)
        db.session.delete(case)
        db.session.commit()

    # -------------------------------------- 执行接口测试 -------------------------------------- #

    @staticmethod
    def execute_test_cases(id_list: list, is_interface: bool) -> TestResult:
        """
        执行测试用例的通用方法
        :param id_list: 接口ID列表或用例ID列表
        :param is_interface: 是否为接口执行模式
        :return: 测试结果
        """
        # 1. 获取待执行用例
        wait_executed_testcase_list = (
            TestCaseServices.get_case_by_interface_list(id_list)
            if is_interface
            else TestCaseServices.get_case_by_case_id_list(id_list)
        )

        # 2. 创建测试结果
        result = TestCaseServices.create_test_result(len(wait_executed_testcase_list))

        # 3. 执行用例并记录结果
        return TestCaseServices.execute_case(result=result, testcases=wait_executed_testcase_list)

    @staticmethod
    def execute_case_by_interface(interface_list: list) -> TestResult:
        """通过接口执行用例（兼容旧代码）"""
        return TestCaseServices.execute_test_cases(interface_list, is_interface=True)

    @staticmethod
    def execute_case_by_case(case_list: list) -> TestResult:
        """直接执行用例（兼容旧代码）"""
        return TestCaseServices.execute_test_cases(case_list, is_interface=False)

    @staticmethod
    def create_test_result(testcase_count: int) -> TestResult:
        """创建测试结果记录"""
        new_result = TestResult(
            result_name=f"测试结果-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            status_of_executions="执行中",
            number_of_executions=testcase_count,
            success_of_executions=0,
            fail_of_executions=0,
            create_user_id=current_user.id
        )
        db.session.add(new_result)
        db.session.commit()
        return new_result

    @staticmethod
    def execute_case(result, testcases: list[TestCase]):
        success_count = 0
        fail_count = 0

        for testcase in testcases:
            interface = testcase.belong_interface
            request_address = interface.interface_address
            request_method = interface.interface_method
            request_headers = json.loads(testcase.headers) if testcase.headers else {}
            request_params = testcase.params
            try:
                response = requests.request(method=request_method,
                                            url=request_address,
                                            headers=request_headers,
                                            data=request_params
                                            )
                response.raise_for_status()
                actual_results = json.dumps(response.json())

                result_item = TestResultItem(
                    interface_id=interface.id,
                    interface_name=interface.interface_name,
                    interface_address=interface.interface_address,
                    interface_method=interface.interface_method,
                    testcase_id=testcase.id,
                    testcase_name=testcase.testcase_name,
                    headers=testcase.headers,
                    params=testcase.params,
                    expected_results=testcase.expected_results,
                    actual_results=actual_results,
                    execution_status=testcase.expected_results in actual_results,
                    result_id=result.id,
                    belong_result=result,
                    create_user_id=current_user.id
                )
                if result_item.execution_status:
                    success_count += 1
                else:
                    fail_count += 1
                db.session.add(result_item)
            except Exception as e:
                fail_count += 1
                db.session.add(TestResultItem(
                    interface_id=interface.id,
                    interface_name=interface.interface_name,
                    interface_address=interface.interface_address,
                    interface_method=interface.interface_method,
                    testcase_id=testcase.id,
                    testcase_name=testcase.testcase_name,
                    headers=testcase.headers,
                    params=testcase.params,
                    expected_results=testcase.expected_results,
                    actual_results=str(e),
                    execution_status=False,
                    result_id=result.id,
                    belong_result=result,
                    create_user_id=current_user.id
                ))

        # 更新结果表数据
        result.status_of_executions = "Finish"
        result.success_of_executions = success_count
        result.fail_of_executions = fail_count
        db.session.commit()
        return result

    # -------------------------------------------------执行结果列表相关------------------------------------------------- #

    @staticmethod
    def get_result_list() -> List[TestResult]:
        """获取所有测试结果（按更新时间排序）"""
        return db.session.scalars(
            select(TestResult)
            .order_by(TestResult.updated_time.desc())
        ).all()

    @staticmethod
    def get_result_list_page(page: int) -> Pagination:
        """获取所有测试结果（按更新时间排序）"""
        return paginate(query=select(TestResult).order_by(TestResult.updated_time.desc()), page=page)

    @staticmethod
    def get_case_result_list(result_id: int) -> TestResult:
        return db.session.scalar(
            select(TestResult)
            .where(TestResult.id == result_id)
        )

    @staticmethod
    def get_case_result_page(result_id: int, page: int):
        return paginate(
            query=select(TestResultItem).where(TestResultItem.result_id == result_id), page=page
        )
