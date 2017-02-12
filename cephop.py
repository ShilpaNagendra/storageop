import swiftclient
'''
create all the global variables required 
for connecting to ceph object store
'''
user = 'testuser:swift'
key = '6Fr3sKEAxUrbAmnHzcWH9FvoD3La7Xf30PcXQjAn'
file_name = 'hello.txt'
container_name = 'swift-container-1'
conn = swiftclient.Connection(user=user,key=key,authurl='http://cephgw/auth',)


'''
---------------------------------------------
Check if the container already exits in the ceph object store
-------------------------------------------
'''
def container_exists(container_name):
	for container in conn.get_account()[1]:
        	print container['name']
	if any(container_name in s['name'] for s in conn.get_account()[1]):
		return True
	return False

'''
---------------------------------------------
Create container in ceph object store, 
if it does not exist already
-------------------------------------------
'''
def create_container():
	if(container_exists(container_name) == False) :
		print('Container does not exist. Creating new container')
		conn.put_container(container_name)
	else:
		print("Container exists.")
'''
---------------------------------------------
Upload objects to ceph object store
-------------------------------------------
'''
def upload_object(object_name):
	print('Request to add object : ' + object_name)
	with open(object_name, 'r') as infile:
        	conn.put_object(container_name, object_name,
                                        contents= infile.read(),
                                        content_type='text/plain')
	print('successfully uploaded object to the container')

'''
---------------------------------------------
Get objects from ceph object store
-------------------------------------------
'''
def get_contents():
	print('Getting ['+ container_name + '] contents')
	for data in conn.get_container(container_name)[1]:
        	print '{0}\t{1}\t{2}'.format(data['name'], data['bytes'], data['last_modified'])


	
'''
---------------------------------------------
download objects from ceph object store
-------------------------------------------
'''
def download_object(src,dest):
	obj_tuple = conn.get_object(container_name, src)
	with open(dest, 'w') as dest_obj:
        	dest_obj.write(obj_tuple[1])

'''
-----------------------------------------------------------------------------------
Define help with the menu 
-----------------------------------------------------------------------------------
'''
def usage():
  print('-------------------------------------------------------------')
  print('Utility to upload / download objects from Ceph')
  print('-------------------------------------------------------------')
  print('cephop [operation] [srcobject] [destobj]')
  print('''
      operation - GET/UPLOAD/DOWNLOAD
      srcobject - object to be uploaded/downloaded
      destobj - object to be saved on local filesystem
      ''')

'''
---------------------------------------------
Start the operations in the ceph object store
-------------------------------------------
'''
def main():
	containerexists = create_container()
	upload_object("src.txt")
	get_contents()
	download_object("src.txt","dest.txt")

#main()		
usage()
