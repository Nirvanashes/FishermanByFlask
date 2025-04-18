import datetime
import json
from flask_login import current_user
from sqlalchemy import select, func
from app.extensions import db
from app.forms import InterfaceTestcaseFrom
from app.schema import TestCase, TestResultItem, TestResult
import requests


class TestCaseServices:
    # -------------------------------------- 数据库获取数据 -------------------------------------- #
    @staticmethod
    def get_all_case():
        return db.session.scalars(TestCase).all()

    @staticmethod
    def get_case_by_interface_id(interface_id):
        return db.session.scalars(select(TestCase).where(TestCase.belong_interface_id == interface_id)).all()

    @staticmethod
    def get_case_by_interface_list(interface_list):
        return db.session.scalars(select(TestCase).where(TestCase.belong_interface_id.in_(interface_list))).all()

    @staticmethod
    def get_case_by_id(case_id):
        return db.session.scalars(select(TestCase).where(TestCase.id == case_id)).all()

    @staticmethod
    def get_case_by_case_id_list(case_id_list):
        return db.session.scalars(select(TestCase).where(TestCase.id.in_(case_id_list))).all()

    # -------------------------------------- 接口交互 -------------------------------------- #

    @staticmethod
    def add_case(form: InterfaceTestcaseFrom):
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
    def edit_case(case_id, form: InterfaceTestcaseFrom):
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
    def execute_case_by_interface(interface_list: list):
        # todo 看后续是否需要转为异步执行
        # 1.获取应该执行的用例,创建执行结果
        wait_executed_testcase_list = TestCaseServices.get_wait_testcase_list_by_interface(interface_list)

        # 2.创建预先执行结果数据
        result = TestCaseServices.create_test_result(interface_list, is_interface=True)

        # 3.执行用例并写入结果快照表
        executed_result = TestCaseServices.execute_case(result, wait_executed_testcase_list)

    @staticmethod
    def execute_case_by_case(case_list: list):
        # todo 看后续是否需要转为异步执行
        # 1.获取应该执行的用例,创建执行结果
        wait_executed_testcase_list = TestCaseServices.get_wait_testcase_list_by_case_id_list(case_list)

        # 2.创建预先执行结果数据
        result = TestCaseServices.create_test_result(wait_executed_testcase_list, is_interface=False)

        # 3.执行用例并写入结果快照表
        executed_result = TestCaseServices.execute_case(result, wait_executed_testcase_list)

    @staticmethod
    def get_wait_testcase_list_by_interface(interface_list):
        wait_executed_testcase_list = [
            testcase
            for interface_id in interface_list
            for testcase in TestCaseServices.get_case_by_interface_id(interface_id)
            if testcase
        ]
        return wait_executed_testcase_list

    @staticmethod
    # todo 考虑性能，后续看是选择使用id还是id_list获取
    def get_wait_testcase_list_by_case_id_list(case_id_list):
        wait_executed_testcase_list = [
            testcase
            for case_id in case_id_list
            for testcase in TestCaseServices.get_case_by_id(case_id)
            if testcase
        ]
        # wait_executed_testcase_list = [
        #     testcase
        #     for testcase in TestCaseServices.get_case_by_case_id_list(case_id_list)
        #     if testcase
        # ]
        return wait_executed_testcase_list

    @staticmethod
    def create_test_result(list, is_interface):
        """通过接口列表或者用例列表获取待执行数量"""
        number_of_executions = 0
        # todo 通过接口列表或者用例列表获取待执行数量，根据is_interface参数判断？
        if is_interface:
            number_of_executions = db.session.scalar(
                select(func.count(TestCase.id))
                .where(TestCase.belong_interface_id.in_(list))
            )
        else:
            number_of_executions = len(list)

        new_result = TestResult(
            result_name=f"测试结果-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            status_of_executions="ING",
            number_of_executions=number_of_executions,
            success_of_executions=0,
            fail_of_executions=0,
            create_user_id=current_user.id
        )
        db.session.add(new_result)
        db.session.commit()
        return new_result

    @staticmethod
    def execute_case(result, wait_executed_testcase_list: list[TestCase]):
        # 将执行成功、失败用例合成一个二元列表返回：
        success_list = fail_list = [TestResultItem]
        success_num = fail_num = 0

        for wait_executed_testcase in wait_executed_testcase_list:
            interface = wait_executed_testcase.belong_interface
            request_address = interface.interface_address
            request_method = interface.interface_method
            if wait_executed_testcase.headers:
                request_headers = json.loads(wait_executed_testcase.headers)
            else:
                request_headers = ""
            request_params = wait_executed_testcase.params
            response = requests.request(method=request_method,
                                        url=request_address,
                                        headers=request_headers,
                                        data=request_params
                                        # params=request_params
                                        )
            actual_results = json.dumps(response.json())
            new_result_item = TestResultItem(
                interface_id=interface.id,
                interface_name=interface.interface_name,
                interface_address=interface.interface_address,
                interface_method=interface.interface_method,
                testcase_id=wait_executed_testcase.id,
                testcase_name=wait_executed_testcase.testcase_name,
                headers=wait_executed_testcase.headers,
                params=wait_executed_testcase.params,
                expected_results=wait_executed_testcase.expected_results,
                actual_results=actual_results,
                execution_status="",
                result_id=result.id,
                belong_result=result,
                create_user_id=current_user.id
            )
            if wait_executed_testcase.expected_results in actual_results:
                new_result_item.execution_status = True
                success_num += 1
                success_list.append(new_result_item)
            else:
                new_result_item.execution_status = False
                fail_num += 1
                fail_list.append(new_result_item)
            db.session.add(new_result_item)
            db.session.commit()

        # 更新结果表数据
        result.status_of_executions = "Finish"
        result.success_of_executions = success_num
        result.fail_of_executions = fail_num
        db.session.commit()
        return result

    # -------------------------------------------------执行结果列表相关------------------------------------------------- #

    @staticmethod
    def get_result_list():
        return db.session.scalars(select(TestResult).order_by(TestResult.updated_time.desc())).all()

    @staticmethod
    def get_case_result_list(result_id):
        return db.get_or_404(TestResult, result_id)
