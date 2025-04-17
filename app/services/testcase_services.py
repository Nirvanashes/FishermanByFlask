import datetime
from flask_login import current_user
from sqlalchemy import select, func
from app.extensions import db
from app.forms import InterfaceTestcaseFrom
from app.schema import TestCase, TestResultItem, TestResult
import requests


class TestCaseServices:
    @staticmethod
    def get_all_case():
        return db.session.scalars(TestCase).all()

    @staticmethod
    def get_case_by_interface(interface_id):
        return db.session.scalars(select(TestCase).where(TestCase.belong_interface_id == interface_id)).all()

    @staticmethod
    def get_case_by_id(case_id):
        return db.get_or_404(TestCase, case_id)

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

    @staticmethod
    def execute_case_by_interface(interface_list: list):
        # 1.获取应该执行的用例,创建执行结果
        wait_executed_testcase_list = TestCaseServices.get_wait_testcase_list(interface_list)

        # 2.创建预先执行结果数据
        result_id = TestCaseServices.create_test_result(interface_list, wait_executed_testcase_list)

        # 3.执行用例并写入结果快照表
        executed_result = TestCaseServices.execute_case(result_id, wait_executed_testcase_list)

        # 4.更新结果表数据
        result = db.get_or_404(TestResult, result_id)
        result.status_of_executions = executed_result.get("status_of_executions")
        result.success_of_executions = executed_result.get("success_num", 0)
        result.fail_of_executions = executed_result.get("fail_num", 0)
        db.session.commit()

    @staticmethod
    def get_wait_testcase_list(interface_list):
        wait_executed_testcase_list = [
            testcase
            for interface_id in interface_list
            for testcase in TestCaseServices.get_case_by_interface(interface_id)
            if testcase
        ]
        return wait_executed_testcase_list

    @staticmethod
    def create_test_result(interface_list, wait_executed_testcase_list):
        """通过接口列表或者用例列表获取待执行数量"""
        number_of_executions = 0
        # 通过接口列表或者用例列表获取待执行数量
        if interface_list:
            number_of_executions = db.session.scalar(
                select(func.count(TestCase.id))
                .where(TestCase.belong_interface_id.in_(interface_list)))
        else:
            number_of_executions = len(wait_executed_testcase_list)

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
        return new_result.id

    @staticmethod
    async def execute_case(result_id, wait_executed_testcase_list: list[TestCase]):
        # 将执行成功、失败用例合成一个二元列表返回：
        success_list = fail_list = [TestResultItem]
        success_num = fail_num = 0

        for wait_executed_testcase in wait_executed_testcase_list:
            interface = wait_executed_testcase.belong_interface
            request_address = interface.interface_address
            request_method = interface.interface_method
            request_headers = wait_executed_testcase.headers
            request_params = wait_executed_testcase.params
            response = requests.request(method=request_method,
                                        url=request_address,
                                        headers=request_headers,
                                        data=request_params,
                                        params=request_params
                                        )
            actual_results = response.text
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
                result_id=result_id
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

        result = {
            "status_of_executions": "Finish",
            "success": success_list,
            "success_num": success_num,
            "fail": fail_list,
            "fail_num": fail_num,
        }
        return result

# -------------------------------------------------执行结果列表相关------------------------------------------------- #

    @staticmethod
    def get_result_list():
        return db.session.scalars(select(TestResult).order_by(TestResult.updated_time.desc())).all()

    @staticmethod
    def get_case_result_list(result_id):
        return db.get_or_404(TestResult, result_id)
