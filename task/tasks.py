from django.core.files.storage import FileSystemStorage

from subprocess import Popen, PIPE
import uuid
import pathlib
import hashlib
import ast

from . import models
from multifist import settings
from multifist.apscheduler import APScheduler


def update_task_job(task):
    pass


def create_task_job(task):
    APScheduler.add_job(func=__task_job,
                        trigger='interval',
                        args=[task],
                        minutes=task.interval,
                        id=task.name)
    task.job = models.aps_models.DjangoJob.objects.get(name=task.name)
    task.save()


def __task_job(task):
    tasks = list()
    for pharty_arg in __pharty_argument_list(task):
        tasks.append(Popen(["pharty2", pharty_arg], stdout=PIPE))

    for job in tasks:
        job.wait()
        __create_web_archive(job, task)


def __create_web_archive(job, task):
    job_args = ast.literal_eval(job.args[1])
    job_return = ast.literal_eval(job.stdout.read().decode('utf-8'))
    web_archive = models.WebArchive()
    web_archive.task = task
    web_archive.web_page = models.WebPage.objects.get(url=list(job_args['url'].keys())[0])
    web_archive.location = f"{list(job_args['url'].values())[0]}.maff"
    web_archive.accessed_time = job_return["Timestamp"][0]
    web_archive.scraped_data = job_return
    web_archive.archive_hash = __hash_file(web_archive.location)
    web_archive.save()


def __hash_file(filename):
    sha = hashlib.sha256()
    with open(filename, "rb") as fd:
        while True:
            data = fd.read(4096)
            if not data:
                break
            sha.update(data)
    return str(sha.hexdigest())


def __pharty_argument_list(task):
    arg_list = list()
    for url in __url_dict_list(task):
        arg_list.append(
            str({'url': url, 'regex': __rule_dict(task)})
        )
    return arg_list


def __rule_dict(task):
    return {rule.name: rule.value for rule in task.rules.all()}


def __url_dict_list(task):
    return [{web_page.url: __gen_filepath(task)} for web_page in task.web_pages.all()]


def __gen_filepath(task):
    task_path = __get_task_path(task)
    web_archive_name = str(uuid.uuid4())
    return str(pathlib.Path(task_path).joinpath(web_archive_name))


def __get_task_path(task):
    task_path = pathlib.Path(settings.MEDIA_ROOT).joinpath(task.name)
    pathlib.Path(task_path).mkdir(parents=True, exist_ok=True)
    return task_path


def pause_task(task_name):
    APScheduler.get_job(task_name).resume()


def resume_task(task_name):
    APScheduler.get_job(task_name).resume()
