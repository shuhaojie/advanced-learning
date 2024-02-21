import uuid


class SSOService:
    def __init__(self):
        pass

    @staticmethod
    def generate_service_ticket():
        # 生成一个随机的Service Ticket
        service_ticket = str(uuid.uuid4())
        return service_ticket
