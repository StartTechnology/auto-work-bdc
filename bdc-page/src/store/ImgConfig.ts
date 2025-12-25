import {ref,computed} from 'vue'
import {defineStore} from 'pinia'
import {PageConfig} from './config'
export const ImgConfig=defineStore('ImgConfig',()=>{
    const pageConfig=PageConfig();

    //服务器请求连接
    //刷新临时目录中的图片信息
    const  temp_img_url=computed(()=>{return pageConfig.server_url+'/img/gettempimg';});
    //获取图片的url拼接+绝对路径
    const get_img_url=computed(()=>{return pageConfig.server_url+'/img/getimg?dir=';});
    //设置图片分类
    const set_img_category_url=computed(()=>{return pageConfig.server_url+'/img/setimgcategory';});
    //同步图片分类目录
    const sync_img_category_url=computed(()=>{return pageConfig.server_url+'/img/syncimgcategory';});
    //清空某个分类图片(目录绝对路径)
    const clear_category_url=computed(()=>{return pageConfig.server_url+'/img/clearcategoryimg';});
    //删除某个分类中的某张图片
    const del_img_category_url=computed(()=>{return pageConfig.server_url+'/img/delcategoryimg';});
    //OCR图片信息
    const ocr_imgs_url=computed(()=>{return pageConfig.server_url+'/img/ocrimgs';});
    //获取临时图片目录文件夹
    //const get_temp_img_dir_url=computed(()=>{return pageConfig.server_url+'/setting/gettempdir';});
    //归档影像url
    const archive_img_url=computed(()=>{return pageConfig.server_url+'/img/archiveimg';});

    //临时图片文件夹的地址
    const temp_img_dir=ref('');
    //图片文件夹地址
    const img_dir=ref('');

    //所有图片的信息(包括分类)
    const images=ref([] as ImgItem[])

    async function getImgConfig(){
        img_dir.value=temp_img_dir.value;
    }

    return {
        temp_img_url,get_img_url,set_img_category_url,sync_img_category_url,clear_category_url,del_img_category_url,ocr_imgs_url,archive_img_url,
        temp_img_dir,img_dir,images,
        getImgConfig
    }
},
{persist:true})

//图片的接口
export interface ImgItem {
    name: string;
    path: string;
    categories: string;
    url: string;
    }