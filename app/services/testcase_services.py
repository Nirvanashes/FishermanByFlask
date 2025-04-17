import datetime
from flask_login import current_user
from sqlalchemy import select, func
from app.extensions import db
from app.forms import InterfaceTestcaseFrom
from app.schema import TestCase, TestResultItem, TestResult


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
        # 1.获取应该执行的用例
        wait_executed_testcase_list = [
            testcase
            for interface_id in interface_list
            for testcase in TestCaseServices.get_case_by_interface(interface_id)
            if testcase
        ]
        number_of_executions = db.session.scalar(
            select(func.count(TestCase.id))
            .where(TestCase.belong_interface_id.in_(interface_list)))

        # 2.先创建执行结果
        new_result = TestResult(
            result_name=f"测试结果-{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            status_of_executions="ING",
            number_of_executions=number_of_executions,
            success_of_executions=0,
            fail_of_executions=0,
            create_user_id=current_user.id
        )
        db.session.add(new_result)
        db.session.commit()
        result_id = new_result.id
        print(result_id)

        # 3.异步执行用例？
        # executed_result = await TestCaseServices.execute_case(wait_executed_testcase_list)
        # 4.写入结果快照表

        # 5.更新结果表数据 #
        # new_result.status_of_executions = "True"
        # new_result.success_of_executions =

    @staticmethod
    async def execute_case(wait_executed_testcase_list: list[TestCase]):
        # 将执行成功、失败用例合成一个二元列表返回：result[success[TestResultItem],fail[TestResultItem]]
        pass

    # -------------------------执行结果列表相关----------------------------------- #
    @staticmethod
    def get_result_list():
        return db.session.scalars(select(TestResult).order_by(TestResult.updated_time.desc()))

    @staticmethod
    def get_case_result_list(result_id):
        return db.get_or_404(TestResult, result_id)
