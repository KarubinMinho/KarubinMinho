import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C


class ResultCallback(CallbackBase):
    """
    重写callbackBase类的部分方法
    refer: http://blog.65535.fun/article/2020/7/9/100.html
    refer: https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
        self.task_ok = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleAPI:
    def __init__(self, connection='smart',
                 remote_user=None,
                 remote_password=None,
                 private_key_file=None,
                 sudo=None, sudo_user=None, ask_sudo_pass=None,
                 module_path=None,
                 become=None,
                 become_method=None,
                 become_user=None,
                 check=False, diff=False,
                 listhosts=None,
                 listtasks=None,
                 listtags=None,
                 verbosity=3,
                 syntax=None,
                 start_at_task=None,
                 inventory=None,
                 timeout=20):
        """
        初始化函数 定义的默认的选项值
        在初始化的时候可以传参 以便覆盖默认选项的值
        """
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            private_key_file=private_key_file,
            sudo=sudo,
            sudo_user=sudo_user,
            ask_sudo_pass=ask_sudo_pass,
            module_path=module_path,
            become=become,
            become_method=become_method,
            become_user=become_user,
            verbosity=verbosity,
            listhosts=listhosts,
            listtasks=listtasks,
            listtags=listtags,
            syntax=syntax,
            start_at_task=start_at_task,
            check=check,
            diff=diff,
            timeout=timeout
        )
        self.inventory = inventory if inventory else '/etc/ansible/hosts'
        self.loader = DataLoader()
        self.inv_obj = InventoryManager(loader=self.loader,
                                        sources=self.inventory)
        self.passwords = remote_password
        self.results_callback = ResultCallback()
        self.variable_manager = VariableManager(self.loader, self.inv_obj)

    def run(self, hosts='localhost',
            gather_facts="no",
            module="ping",
            args='',
            task_time=0):
        play_source = dict(
            name="Ad-hoc",
            hosts=hosts,
            gather_facts=gather_facts,
            tasks=[{"action": {"module": module, "args": args},
                    "async": task_time,
                    "poll": 0}])
        play = Play().load(play_source,
                           variable_manager=self.variable_manager,
                           loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(inventory=self.inv_obj,
                                   variable_manager=self.variable_manager,
                                   loader=self.loader,
                                   passwords=self.passwords,
                                   stdout_callback=self.results_callback)
            tqm.run(play)

        finally:
            if tqm is not None:
                tqm.cleanup()
                shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def playbook(self, playbooks):
        """
        Keyword arguments:
        playbooks -- 需要是一个列表类型
        """
        from ansible.executor.playbook_executor import PlaybookExecutor

        playbook = PlaybookExecutor(playbooks=playbooks,
                                    inventory=self.inv_obj,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    passwords=self.passwords)
        # 使用回调函数
        playbook._tqm._stdout_callback = self.results_callback
        playbook.run()

    def get_result(self):
        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        # print(self.results_callback.host_ok)
        for host, result in self.results_callback.host_ok.items():
            result_raw['success'][host] = result._result
        for host, result in self.results_callback.host_failed.items():
            result_raw['failed'][host] = result._result
        for host, result in self.results_callback.host_unreachable.items():
            result_raw['unreachable'][host] = result._result
        # 最终打印结果，并且使用 JSON 继续格式化
        # print(json.dumps(result_raw, indent=4))
        return json.dumps(result_raw)
