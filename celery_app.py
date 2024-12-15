from extensions import celery

@celery.task
def send_contract_email(contract_info):
    print(f"Надсилаю email про контракт: {contract_info}")
    return True