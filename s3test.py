import boto
import boto.s3.connection
access_key = 'C3KE0NTK63UVQWZ3H6IP'
#'AI0PJDPCIYZ665MW88W9R'
secret_key = 'NuxV6qnUD5yEo2Hd2Qu8AJtO9hOWZCIl2keG58vk'
#'dxaXZ8U90SXydYzyS5ivamEP20hkLSUViiaR+ZDA'
conn = boto.connect_s3(
aws_access_key_id = access_key,
aws_secret_access_key = secret_key,
host = 'cephgw',
is_secure=False,
calling_format = boto.s3.connection.OrdinaryCallingFormat(),
)
bucket = conn.create_bucket('my-new-bucket')
for bucket in conn.get_all_buckets():
	print "{name}\t{created}".format(
		name = bucket.name,
		created = bucket.creation_date,
)
