import ast
import boto3
import logging
import os
import sys
import traceback

LOG_FILE_NAME = 'output.log'

# Change region to match with the default region that you setup when configuring your AWS CLI
REGION = 'us-west-2'

class S3Handler:
    """S3 handler."""

    def __init__(self):
        self.client = boto3.client('s3')

        logging.basicConfig(filename=LOG_FILE_NAME,
                            level=logging.DEBUG, filemode='w',
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        self.logger = logging.getLogger("S3Handler")

    def help(self):
        print("Supported Commands:")
        print("1. createdir <bucket_name>")
        print("2. upload <source_file_name> <bucket_name> [<dest_object_name>]")
        print("3. download <dest_object_name> <bucket_name> [<source_file_name>]")
        print("4. delete <dest_object_name> <bucket_name>")
        print("5. deletedir <bucket_name>")
        print("6. find <pattern> <bucket_name> -- e.g.: find txt bucket1 --")
        print("7. listdir [<bucket_name>]")
    
    def _error_messages(self, issue):
        error_message_dict = {}
        error_message_dict['operation_not_permitted'] = 'Not authorized to access resource.'
        error_message_dict['incorrect_parameter_number'] = 'Incorrect number of parameters provided'
        error_message_dict['not_implemented'] = 'Functionality not implemented yet!'
        error_message_dict['bucket_name_exists'] = 'Directory already exists.'
        error_message_dict['bucket_name_empty'] = 'Directory name cannot be empty.'
        error_message_dict['non_empty_bucket'] = 'Directory is not empty.'
        error_message_dict['missing_source_file'] = 'Source file cannot be found.'
        error_message_dict['non_existent_bucket'] = 'Directory does not exist.'
        error_message_dict['non_existent_object'] = 'Destination File does not exist.'
        error_message_dict['unknown_error'] = 'Something was not correct with the request. Try again.'

        if issue:
            return error_message_dict[issue]
        else:
            return error_message['unknown_error']

    def _get_file_extension(self, file_name):
        if os.path.exists(file_name):
            return os.path.splitext(file_name)

    def _get(self, bucket_name):
        response = ''
        try:
            response = self.client.head_bucket(Bucket=bucket_name)
        except Exception as e:
            # print(e)
            # traceback.print_exc(file=sys.stdout)
            
            response_code = e.response['Error']['Code']
            if response_code == '404':
                return False
            elif response_code == '200':
                return True
            else:
                raise e
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False

    def createdir(self, bucket_name):
        if not bucket_name:
            return self._error_messages('bucket_name_empty')

        try:
            if self._get(bucket_name):
                return self._error_messages('bucket_name_exists')
            self.client.create_bucket(Bucket=bucket_name,
                                      CreateBucketConfiguration={'LocationConstraint': REGION})
        except Exception as e:
            print(e)
            raise e

        # Success response
        operation_successful = ('Directory %s created.' % bucket_name)
        return operation_successful

    def listdir(self, bucket_name):
        # If bucket_name is provided, check that bucket exits.
        
        # If bucket_name is empty then display the names of all the buckets
        
        # If bucket_name is provided then display the names of all objects in the bucket
        return self._error_messages('not_implemented')

    def upload(self, source_file_name, bucket_name, dest_object_name=''):
        # 1. Parameter Validation
        #    - source_file_name exits in current directory
        #    - bucket_name exists
        # 2. If dest_object_name is not specified then use the source_file_name as dest_object_name

        # 3. SDK call
        #    - When uploading the source_file_name and add it to object's meta-data

        # Success response
        # operation_successful = ('File %s uploaded to directory %s.' % (source_file_name, bucket_name))

        return self._error_messages('not_implemented')


    def download(self, dest_object_name, bucket_name, source_file_name=''):
        # if source_file_name is not specified then use the dest_object_name as the source_file_name
        # If the current directory already contains a file with source_file_name then move it as a backup
        # with following format: <source_file_name.bak.current_time_stamp_in_millis>
        
        # Parameter Validation
        
        # SDK Call

        # Success response
        # operation_successful = ('File %s downloaded from directory %s.' % (dest_object_name, bucket_name))

        return self._error_messages('not_implemented')


    def delete(self, dest_object_name, bucket_name):
        
        # Success response
        # operation_successful = ('File %s deleted from directory %s.' % (dest_object_name, bucket_name))
        
        return self._error_messages('not_implemented')


    def deletedir(self, bucket_name):
        # Delete the bucket only if it is empty
        
        # Success response
        # operation_successful = ("Deleted directory %s." % bucket_name)
        
        return self._error_messages('not_implemented')


    def find(self, pattern, bucket_name=''):
        # Return object names that match the given file extension

        # If bucket_name is specified then search for objects in that bucket.
        # If bucket_name is empty then search all buckets
        

        
        return self._error_messages('not_implemented')


    def dispatch(self, command_string):
        parts = command_string.split(" ")
        response = ''

        if parts[0] == 'createdir':
            # Figure out bucket_name from command_string
            if len(parts) > 1:
                bucket_name = parts[1]
                response = self.createdir(bucket_name)
            else:
                # Parameter Validation
                # - Bucket name is not empty
                response = self._error_messages('bucket_name_empty')
        elif parts[0] == 'upload':
            # Figure out parameters from command_string
            # source_file_name and bucket_name are compulsory; dest_object_name is optional
            # Use self._error_messages['incorrect_parameter_number'] if number of parameters is less
            # than number of compulsory parameters
            source_file_name = ''
            bucket_name = ''
            dest_object_name = ''
            response = self.upload(source_file_name, bucket_name, dest_object_name)
        elif parts[0] == 'download':
            # Figure out parameters from command_string
            # dest_object_name and bucket_name are compulsory; source_file_name is optional
            # Use self._error_messages['incorrect_parameter_number'] if number of parameters is less
            # than number of compulsory parameters
            source_file_name = ''
            bucket_name = ''
            dest_object_name = ''
            response = self.download(dest_object_name, bucket_name, source_file_name)
        elif parts[0] == 'delete':
            dest_object_name = ''
            bucket_name = ''
            response = self.delete(dest_object_name, bucket_name)
        elif parts[0] == 'deletedir':
            bucket_name = ''
            response = self.deletedir(bucket_name)
        elif parts[0] == 'find':
            pattern = ''
            bucket_name = ''
            response = self.find(pattern, bucket_name)
        elif parts[0] == 'listdir':
            bucket_name = ''
            response = self.listdir(bucket_name)
        else:
            response = "Command not recognized."
        return response


def main():

    s3_handler = S3Handler()
    
    while True:
        try:
            command_string = ''
            if sys.version_info[0] < 3:
                command_string = raw_input("Enter command ('help' to see all commands, 'exit' to quit)>")
            else:
                command_string = input("Enter command ('help' to see all commands, 'exit' to quit)>")
    
            # Remove multiple whitespaces, if they exist
            command_string = " ".join(command_string.split())
            
            if command_string == 'exit':
                print("Good bye!")
                exit()
            elif command_string == 'help':
                s3_handler.help()
            else:
                response = s3_handler.dispatch(command_string)
                print(response)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
