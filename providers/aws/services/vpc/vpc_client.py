from providers.aws.lib.audit_info.audit_info import current_audit_info
from providers.aws.services.vpc.vpc_service import VPC

vpc_client = VPC(current_audit_info)
