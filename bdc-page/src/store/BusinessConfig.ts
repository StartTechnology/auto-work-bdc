import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { PageConfig } from "./config";
export const BusinessConfig = defineStore(
  "BusinessConfig",
  () => {
    const pageConfig= PageConfig();
    //OCR类型
    const OCRTYPE = ref([
  { value: "1", name: "身份证",is_loading:false },
  { value: "2", name: "合同编号",is_loading:false },
   { value: "3", name: "贷款金额",is_loading:false },
   { value: "4", name: "贷款期限",is_loading:false },
   { value: "5", name: "抵押登记证号",is_loading:false },
   { value: "6", name: "房产证号",is_loading:false },
]);

    //业务类型
    const business_type = ref("");
    //业务所需材料
    const business_materials = ref([] as string[]);

    const customer = ref([{name:'',id:'',phone:''},] as CustomerInfo[]);


    //贷款信息：金额，期限，合同编号，种类
    const loan_type = ref("");
    const loan_amount = ref([] as string[]);

    const loan_tream = ref([] as Tream[]);
    const loan_contract = ref([] as string[]);
    //担保范围
    const loan_guarantee= ref('')

    //抵押信息：房产证编号 抵押证明编号
    const certificate = ref(['',] as string[]);
    //客户经理
    const loan_manager = ref("");

    //开发商信息
    const developer_info = ref({name:'',id:'',phone:''} as CustomerInfo);
    //购房合同
    const customer_contract = ref("");

    //请求URL
    const get_loan_type_url=computed(()=>{return pageConfig.server_url+'/setting/getloantype'});
    const get_loan_guarantee_url=computed(()=>{return pageConfig.server_url+'/setting/getguaranteescope'});
    const get_loan_manager_url=computed(()=>{return pageConfig.server_url+'/setting/getcustomermanager'});
    const get_developer_info_url=computed(()=>{return pageConfig.server_url+'/setting/getdevelopers'});
    //提交任务URl
    const submit_task_url=computed(()=>{return pageConfig.server_url+'/pushtask/pushtask'});
    //写入数据url
    const write_data_url=computed(()=>{return pageConfig.server_url+'/pushtask/towps'});


    //重置数据
    function reset(){
      business_type.value='';
      business_materials.value=[];
      customer.value=[{name:'',id:'',phone:''},];
      loan_type.value='';
      loan_amount.value=[];
      loan_tream.value=[];
      loan_contract.value=[];
      loan_guarantee.value='';
      certificate.value=['',];
      loan_manager.value='';
      developer_info.value={name:'',id:'',phone:''};
      customer_contract.value='';
    }

    return {
      OCRTYPE,
      business_type,
      business_materials,
      customer,
      loan_type,
      loan_amount,
      loan_tream,
      loan_contract,
      loan_guarantee,
      certificate,
      loan_manager,
      developer_info,
      customer_contract,
      
      get_loan_type_url,get_loan_guarantee_url,get_loan_manager_url,get_developer_info_url,submit_task_url,write_data_url,

      reset
      
    };
  },
  { persist: true }
);


//客户信息：姓名，身份证,电话号码
export interface CustomerInfo {
  name: string;
  id: string;
  phone: string;
}
//日期
export interface Tream {
  start: string;
  end: string;
}
