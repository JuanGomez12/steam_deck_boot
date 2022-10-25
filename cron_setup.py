import getpass
import subprocess
import logging


class CronJobManager:
    def __init__(self, user: str, cron_job: str) -> None:
        self.user = user
        self.cron_job = cron_job

    def create_cron_job(self) -> int:
        if not self.check_cron_job_status():
            logging.info(f"Cron job: '{self.cron_job}' does not exist, creating")
            filter = "".join([chr(i) for i in range(1, 32)])
            translation_table = str.maketrans("", "", filter)
            cron_job_creation = subprocess.run(
                f'(crontab -u {self.user} -l; echo "{self.cron_job}" ) | crontab -u {self.user} -',
                capture_output=True,
                shell=True,
            )
            status = cron_job_creation.returncode
            if status != 0:
                stdout = cron_job_creation.stdout.decode("utf-8")
                stdout.translate(translation_table)
                stderr = cron_job_creation.stderr.decode("utf-8")
                stderr = stderr.translate(translation_table)
                raise RuntimeError(
                    f"Error creating cron job - stdout:'{stdout}', stderr:'{stderr}'"
                )
        else:
            logging.info(f"Cron job: '{self.cron_job}' already exists")
            status = 0
        return status

    def check_cron_job_status(self) -> bool:
        filter = "".join([chr(i) for i in range(1, 32)])
        translation_table = str.maketrans("", "", filter)

        cron_subprocess = subprocess.run(
            f"crontab -u {self.user} -l".split(), capture_output=True
        )
        cron_string = cron_subprocess.stdout.decode("utf-8")
        cron_string = cron_string.translate(translation_table)

        cron_job_status = cron_job.replace(" ", "") in cron_string.replace(" ", "")
        return cron_job_status


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    user = getpass.getuser()
    cron_job = (
        "@reboot python3 ~/.steam/root/config/uioverrides/animation_randomizer.py"
    )
    cron_job_manager = CronJobManager(user, cron_job)
    cron_job_manager.create_cron_job()
