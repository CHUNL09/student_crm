perm_dic = {
    # 角色 admin 的映射关系
    'view_index': ['view_data','GET',[]],
    'view_records': ['view_data','POST',['action',]],
    'view_statics': ['view_statics','GET',[]],
    'search_statics': ['view_statics','POST',[]],
    # 删除记录的权限
    'del_records': ['delete_data','POST',['table_val','pk_val','action']],



    # 角色 consultant 的映射关系
}



from django.core.urlresolvers import resolve
from django.shortcuts import render,redirect,HttpResponse


def perm_check(*args,**kwargs):
    request = args[0]
    url_resovle_obj = resolve(request.path_info)
    current_url_namespace = url_resovle_obj.url_name
    print("url namespace:",current_url_namespace)
    matched_flag = False # find matched perm item
    matched_perm_key = None
    if current_url_namespace is not None:
        print("checking permissions...")
        for perm_key in perm_dic:
            perm_val = perm_dic[perm_key]
            if len(perm_val) == 3:
                url_namespace,request_method,request_args = perm_val
                print(url_namespace,current_url_namespace)
                if url_namespace == current_url_namespace:
                    if request.method == request_method:
                        if not request_args:
                            matched_flag = True
                            matched_perm_key = perm_key
                            print('matched...')
                            break
                        else:
                            for request_arg in request_args:
                                request_method_func = getattr(request,request_method)
                                if request_method_func.get(request_arg) is not None:
                                    matched_flag = True
                                else:
                                    matched_flag = False
                                    print("request arg [%s] not matched" % request_arg)
                                    break
                            if matched_flag == True:
                                print("--passed permission check here--")
                                matched_perm_key = perm_key
                                break

    else:#permission doesn't work
        return True

    if matched_flag == True:
        #pass permission check
        perm_str = "app01.%s" %(matched_perm_key)
        if request.user.has_perm(perm_str):
            print("\033[42;1m--------passed permission check----\033[0m")
            return True
        else:
            print("\033[41;1m ----- no permission ----\033[0m")
            print(request.user,perm_str)
            return False
    else:
        print("\033[41;1m ----- no matched permission  ----\033[0m")
def check_permission(func):

    def wrapper(*args,**kwargs):
        print("---start check perms",args[0])
        if not perm_check(*args,**kwargs):
            return render(args[0],'error.html',{'errors':'403 link,No permissions'})
        return func(*args,**kwargs)
    return wrapper

