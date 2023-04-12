from requests import get, post, delete
from requests import Response
from os import path, getcwd

#docx_headers = {"Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document; charset=utf-8"}
#csv_headers = {"Content-Type": "text/csv; charset=utf-8"}
#zip_headers = {"Content-Type": "application/zip; charset=utf-8"}

class APIworker:

    def __update_file_dic(
            self, dictionary: dict, key: str, full_filename: str):
        dictionary.update({key: None})
        if full_filename != None and full_filename != "": 
            if path.exists(full_filename):
                dictionary.update(
                    {key: open(full_filename, 'rb')})
                
    def get_file(self, api_str: str) -> Response:
        response: Response = \
            get(r"http://127.0.0.1:8080" + api_str, stream=True)
        if response.status_code == 200:
            print(response.headers)
            content_disposition_list: list = \
                response.headers["Content-Disposition"].split(";")
            download_filename: str
            for item in content_disposition_list:               
                if "filename=" in item:
                    download_filename = item.split("=")[1].rstrip()
                    break
            print(download_filename)
            save_path: str = \
                path.join(path.abspath(getcwd()), 
                        "downloads", download_filename)
            print(save_path)
            with open(save_path, "wb") as fhandler:
                fhandler.write(response.content)
            return response
        return None

    def post_file(self, file_type: str,
                  full_filename: str) -> Response:
        if file_type == "document" or file_type == "dictionary_file":
            file_dic: dict = {}
            api_str: str
            if file_type == "document":
                api_str = "/document/" \
                          + path.split(full_filename)[1] \
                                .replace(".docx", "")
                self.__update_file_dic(
                    file_dic, "document", full_filename)
            elif file_type == "dictionary_file":
                api_str = "/dictionary_file/" \
                          + path.split(full_filename)[1] \
                                .replace(".csv", "")
                self.__update_file_dic(
                    file_dic, "dictionary_file", full_filename)
            return post(r"http://127.0.0.1:8080" + api_str,
                        files=file_dic, stream=True)
        return None
    
    def get_files(self, full_doc_path: str, full_dic_path: str, \
                  query_component: str):   
        if full_doc_path != None and full_dic_path == None:
            doc_name: str = \
                path.split(full_doc_path)[1].split(".")[0]
            status_code = self.post_file(
                              "document", 
                              full_doc_path).status_code
            if status_code == 200:
                if query_component != "?":
                    self.get_file("/document/" \
                                  + doc_name \
                                  + "/fixed-document-file" \
                                  + query_component) 
                else:
                    self.get_file("/document/" \
                                  + doc_name \
                                  + "/dictionary-file")
            self.delete_tmp_files()

    def replace_fields_in_document(
            self, full_doc_path: str,  full_dic_path: str,
            query_component: str):
        if full_doc_path != None and full_dic_path != None:
            doc_name: str = \
                path.split(full_doc_path)[1].split(".")[0]
            dic_name: str = \
                path.split(full_dic_path)[1].split(".")[0]
            post_doc_status_code = \
                self.post_file(
                    "document", 
                    full_doc_path).status_code
            post_dic_status_code = \
                self.post_file(
                    "dictionary_file", 
                    full_dic_path).status_code
            if post_doc_status_code == 200 \
                   and post_dic_status_code == 200:
                self.get_file(
                    "/document/" + doc_name + "/" + dic_name + "/" \
                    + "fixed-document" + query_component)
            self.delete_tmp_files()

    def delete_tmp_files(self) -> Response:
        return delete(r"http://127.0.0.1:8080/cleaning")