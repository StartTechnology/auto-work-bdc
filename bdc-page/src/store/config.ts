import {ref,computed} from 'vue'
import {defineStore} from 'pinia'
import axios from 'axios';
export const PageConfig=defineStore('PageConfig',()=>{
    const server_url=ref(`http://localhost:8002`);
    const work_dir=ref(`D:/work`);

    //业务配置
    const business_config_colums=ref([]);
    const business_config_data=ref([]);
    const businessXlsx_path=ref('');

    //服务器请求url连接
    const work_dir_url=computed(()=>{return server_url.value+'/setting/getworkdir'});
    const business_config_url=computed(()=>{return server_url.value+'/setting/getbusinessconfig'});
    //设置业务参数url 服务器直接打开文件
    const business_config_set_url=computed(()=>{return server_url.value+'/setting/openbusinessconfig'});
    //设置工作目录url
    const work_dir_set_url=computed(()=>{return server_url.value+'/setting/setworkdir'});
    //读取业务xlsx路径
    const get_businessXlsx_url=computed(()=>{
        return server_url.value+'/setting/getbusinessxlsx';
    });
    //保存业务xlsx路径
    const set_businessXlsx_url=computed(()=>{
        return server_url.value+'/setting/setbusinessxlsx';
    })

    
    //从服务器获取配置信息
    async function getConfigFromServer():Promise<void>
    {
        const [workDirResponse, businessConfigResponse] = await Promise.all([
                axios.get(work_dir_url.value),
                axios.get(business_config_url.value)
            ]);
        // 赋值更新状态
        work_dir.value = workDirResponse.data;
        business_config_colums.value=businessConfigResponse.data.columns;
        business_config_data.value=businessConfigResponse.data.data;
    }
    //保存工作目录信息到服务器
    async function setWorkDir():Promise<void> {
        axios.post(work_dir_set_url.value,{'path':work_dir.value})
    }

    return {
        server_url,work_dir,
        business_config_colums,business_config_data,businessXlsx_path,

        work_dir_url,business_config_url,business_config_set_url,work_dir_set_url,get_businessXlsx_url,set_businessXlsx_url,
        

        getConfigFromServer,setWorkDir

    };
},
{persist:true});

