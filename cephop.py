import swiftclient
import argparse
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
  '''
  for container in conn.get_account()[1]:
        	print (container['name'])
  '''
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
'''
---------------------------------------------
Upload objects to ceph object store
-------------------------------------------
'''
def upload_object(object_name):
  print('Request to add object : ' + object_name)
  create_container()
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
  #print('Getting ['+ container_name + '] contents')
  create_container()
  for data in conn.get_container(container_name)[1]:
        	print ('{0}\t{1}\t{2}'.format(data['name'], data['bytes'],
                data['last_modified']))


	
'''
---------------------------------------------
download objects from ceph object store
-------------------------------------------
'''
def download_object(src,dest):
  create_container()
  obj_tuple = conn.get_object(container_name, src)
  with open(dest, 'w') as dest_obj:
        	dest_obj.write(obj_tuple[1])
  print('successfully downloaded object to the container')

'''
-----------------------------------------------------------------------------------
Define help with the menu 
-----------------------------------------------------------------------------------
'''
def usage():
  print('-------------------------------------------------------------')
  print('Utility to upload / download objects from Ceph')
  print('-------------------------------------------------------------')
  print('cephop [operation] [srcobject] [destobj] [h]')
  print('''
      operation - view/upload/download
      srcobject - object to be uploaded/downloaded
      destobj - object to be saved on local filesystem
      ''')
  print(''' Examples
      To list all files in the container
        cephop view
      To upload an object
        cephop upload obj1
      To download an object
        cephop download srcobj destobj
      ''')
  print('-------------------------------------------------------------')

'''
Using argparser to display args
'''
def arg_usage():
  parser = argparse.ArgumentParser()
  parser.add_argument("-v","--view",help="view the files in the storage",
      action='store_true')
  parser.add_argument("-u","--upload",help="upload the object to ceph",
      nargs=1,type = str)
  parser.add_argument("-d","--download",help="download the object from ceph",
      nargs=2)
  args = parser.parse_args()
  if args.view:
    get_contents()
  elif args.upload:
    file_name = args.upload[0]
    upload_object(file_name)
  elif args.download:
    src=args.download[0]
    dest=args.download[1]
    download_object(src,dest)
  else :
    print('Unknown option.Try -h')


'''
---------------------------------------------
Start the operations in the ceph object store
-------------------------------------------
'''
def main():
  arg_usage()
  '''
  usage()
  upload_object("src.txt")
  get_contents()
  download_object("src.txt","dest.txt")
  '''
main()		


