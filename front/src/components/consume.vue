
import func from './vue-temp/vue-editor-bridge';
import { try } from 'q';
<template>
<div>
    <el-row type="flex" class="row-bg" justify="center">
  <el-col :span="4"> <el-button
              @click="applycomsume({},topic_name,cluster,0,topic,brokers, false)"
              type="primary"
              style="font-size: 16px;padding: 11px"
            >新建消费</el-button></el-col>
  <el-col :span="6"></el-col>
  <el-col :span="10">
      <el-row :gutter="20">
  <el-col :span="16"><el-autocomplete
                  class="inline-input"
                  v-model="group_id"
                  style="width:100%;"
                  :fetch-suggestions="querySearch"
                   prefix-icon="el-icon-search"
                  placeholder="请输入GroupID"
                ></el-autocomplete></el-col>
  <el-col :span="8"> <el-button
                type="primary"
                 @click="load_data"
                style="padding: 11px;
  font-size: 16px;"
              >确 定</el-button></el-col>
</el-row>
     </el-col>
</el-row>
<el-table :data="table_data1" style="padding:30px 30px 0 30px;margin-top:30px;" :header-cell-style="{background:'#e5e9f2'}">
          
        <el-table-column label="Consume名称" min-width="8" width="261" align="center" show-overflow-tooltip>
          <template slot-scope="scope">
              {{scope.row.consumer_group_name}}
          </template>
        </el-table-column>

        <el-table-column prop="consumer_describe" label="描述" min-width="12" align="center"></el-table-column>

        <el-table-column prop="consumer_client" label="消费客户端" min-width="6" align="center"></el-table-column>

        <el-table-column prop="consumer_user" label="申请人" min-width="7" align="center"></el-table-column>

        <el-table-column label="消费Broker List" width="270" align="center">
           <template slot-scope="scope">
               <div v-if="scope.row.consumer_broker_list">
              <div v-for="broker in scope.row.consumer_broker_list.split(',')">{{broker}}</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="操作" min-width="12" align="center">
          <template slot-scope="scope">
              <div style="margin-bottom: 4px">
              <el-button
                type="success"
                style="padding: 5px 16px;font-size: 13px"
                :disabled="scope.row.status ===0"
                @click="consumerproduct(scope.row.consumer_group_name)"
              >消费监控</el-button>
            </div>
            <div style="margin-bottom: 4px">
              <el-button
                type="success"
                style="padding: 5px 16px;font-size: 13px"
                @click="deleteconsumer(scope.row.consumer_group_name,scope.row.id, scope.row.index)"
              >删除消费</el-button>
            </div>
              <el-button
                type="success"
                style="padding: 5px 16px;font-size: 13px"
                @click="applycomsume(scope.row,topic_name,cluster,0,topic,brokers,true)"
              >编辑消费</el-button>
          </template>
        </el-table-column>
      </el-table>
<el-dialog title="消费监控" :visible.sync="consumelog" width="80%">
  <el-table
        v-loading="loading"
        element-loading-text="数据量较大，加载时间可能较长…"
        :data="table_data"
        :empty-text="empty_text"
        style="width: 100%"
        height="250"
         :row-class-name="tableRowClassName"
      >
        <el-table-column prop="time" label="Time" min-width="10" align="center"></el-table-column>
        <el-table-column prop="commit_offset" label="currentOffset" min-width="8" align="center"></el-table-column>

        <el-table-column prop="end_offsets" label="logEndOffset" min-width="8" align="center"></el-table-column>

        <el-table-column prop="lag" label="Lag" min-width="6" align="center" class-name="lag-color"></el-table-column>

        <el-table-column prop="partition" label="Partition" min-width="5" align="center"></el-table-column>
      </el-table>
  <div slot="footer" class="dialog-footer">
    <el-button @click="consumelog = false">取 消</el-button>
  </div>
</el-dialog>

<el-dialog 
 :title="is_update?'编辑消费kafka的Groupid':'申请消费kafka的Groupid'"
:visible.sync="addDialogVisible1" @close="resetForm1()">
        <hr style="margin: -20px 0 25px 0">
        <el-form :model="consumer_form" :rules="rules1" ref="dialog_f1" v-loading="form_loading">
          <el-form-item prop="consumer_group_name" label="申请消费group名称" label-width="160px">
            <el-col :span="8">
              <el-input v-model="consumer_form.consumer_group_name" :disabled="is_update"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="consumer_client" label="申请消费client" label-width="160px">
            <el-col :span="6">
              <el-select v-model="consumer_form.consumer_client">
                <el-option v-for="item in kafka_client" :label="item" :value="item" :key="item"></el-option>
              </el-select>
            </el-col>
          </el-form-item>
          <el-form-item prop="consumer_describe" label="日志消费用途描述" label-width="160px">
            <el-col :span="20">
              <el-input v-model="consumer_form.consumer_describe"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="consumer_cluster" label="kafka集群名称" label-width="160px">
            <el-col :span="12">
              <el-input
                v-model="consumer_form.consumer_cluster"
                placeholder="kafka集群名称"
                disabled
              ></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="consumer_topic" label="topic名称" label-width="160px">
            <el-col :span="12">
              <el-input
                v-model="consumer_form.topic_name"
                placeholder="topic名称"
                disabled
              ></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="consumer_user" label="Group负责人" label-width="160px">
            <el-col :span="12">
              <el-input
                v-model="consumer_form.consumer_user"
                placeholder="Group负责人"
                disabled
              ></el-input>
            </el-col>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button v-if="!is_update"
            type="success"
            @click="addComsumerGroup"
          >确 定</el-button>
           <el-button v-else
            type="success"
            @click="updateComsumerGroup"
          >确 定</el-button>
          <el-button @click="resetForm1">取 消</el-button>
        </div>
      </el-dialog>
   
   <div style="text-align: center; margin: 20px 0 40px 0;">
      <el-button @click="redirect" type="info">返 回</el-button>
    </div>

</div>
</template>

<script>
export default {
data() {
    return {
        kafka_client: ["Go", "Python", "C++", "Java", "Filebeat", "Flink", "Lua"],
        rules1: {
        consumer_group_name: [
          {
            required: true,
            message: "该项不能为空",
            trigger: "blur"
          }
        ],
        consumer_client: [
          {
            required: true,
            message: "该项不能为空",
            trigger: "blur"
          }
        ],
        consumer_describe: [
          {
            required: true,
            message: "该项不能为空",
            trigger: "blur"
          }
        ]
      },
        form_loading:false,
        addDialogVisible1:false,
        consumer_form: {
        consumer_group_name: "",
        consumer_client: "",
        consumer_describe: "",
        consumer_cluster: "",
        consumer_topic: 0,
        topic_name:'',
        consumer_user: this.$cookie.get("username"),
        topic_id: "",
        consumer_broker_list: ""
      },
      group_name: "",
      topic_name:"",
      consumelog:false,
      topic: "",
      cluster: "",
      group_id: "",
      date_range: "",
      table_data1: [],
      table_data:[],
      group_list: [],
      empty_text: "请输入Group ID显示数据",
      loading: false,
      prepage: 0,
      switch1: 0,
      echarts: true,
      is_update:false
    };
  },
  mounted: function() {
    this.init();
  },
  methods: {
      tableRowClassName({row, rowIndex}) {
        if (rowIndex === 0) {
          return 'success-row';
        } 
        return '';
      
    },
     redirect: function() {
      window.history.go(-1);
    },
    init: function() {
        this.topic = this.$route.query.topic;
        this.cluster = this.$route.query.cluster;
        this.partition = this.$route.query.partition;
        this.topic_name = this.$route.query.topic_name;
        this.brokers = this.$route.query.brokers;
     this.axios.get('/kops/consumergroup/',{
      params:{
         consumer_topic: this.topic,
         consumer_cluster: this.cluster,
      }
    }).then(res=>{
      console.log(res.data)
        let a = res.data;
        let _data = [];
        let children = []
        if (a){
        a.forEach((item,index)=>{
          children.push({
            "value":item.fields.consumer_group_name
          })
          let data_temp = item.fields;
            data_temp["id"] = item.pk;
            data_temp["index"] = index;
            _data.push(data_temp);
        })}
        console.log(children)
        console.log(_data)
       this.group_list = children;
        this.table_data1 = _data;

    })
    },
    load_data: function() {
      let that = this;
        that.loading = true;
      that.axios
        .get("/kops/consumergroup/", {
          params: {
            consumer_topic: this.topic,
            consumer_cluster: that.cluster,
            consumer_group_name: that.group_id
          }
        })
        .then(res => {
          console.log(res.data);
          let data = res.data;
          let _data = [];

          data.forEach((item, index) => {
            let data_temp = item.fields;
            data_temp["id"] = item.pk;
            data_temp["index"] = index;
            _data.push(data_temp);
          });
          console.log(_data);
          // if ((res.status = 200)) {
          that.table_data1 = _data;
          console.log(_data)
        //   that.consumerproduct(_data[0]["consumer_group_name"])
              
          
        });
    },
      consumerproduct:function(name){
          let that =this;
          that.axios.put('/kops/consumergroup/'+name+'/',{"partition":that.partition,"topic_name":this.topic_name}).then(res=>{
            this.table_data = res.data.data
            console.log("&&&&&&&&&",res)
            that.consumelog =true;
          })
      },
      querySearch:function(queryString, cb) {
        var groups = this.group_list;
        var results = queryString ? groups.filter(this.createFilter(queryString)) : groups;
        cb(results);
      },
      createFilter:function(queryString) {
        return (group) => {
          console.log(group)
          return (group.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
        };
      },

    redirect: function() {
      window.history.go(-1);
    },
     applycomsume: function(dict,topic_name, cluster, status, topicid, brokerlist, flag) {
      let that = this;
        if(! flag){
        that.consumer_form.consumer_cluster = cluster;
        that.consumer_form.consumer_topic = topicid;
        that.consumer_form.topic_name = topic_name;
        that.consumer_form.topic_id = topicid;
        that.consumer_form.consumer_broker_list = brokerlist;
        that.consumer_form.consumer_user = that.$cookie.get('username')
        that.addDialogVisible1 = true;
        that.is_update = false
        console.log(topic_name, cluster, status, topicid, brokerlist)
        }
        else{
            console.log("*******",dict)
            that.consumer_form.consumer_cluster = cluster;
        that.consumer_form.consumer_topic = topicid;
        that.consumer_form.topic_name = topic_name;
        that.consumer_form.topic_id = topicid;
        that.consumer_form.consumer_broker_list = brokerlist;
        that.consumer_form.consumer_user = dict['consumer_user']
        that.consumer_form.consumer_group_name = dict.consumer_group_name
        that.consumer_form.consumer_client = dict.consumer_client
        that.consumer_form.consumer_describe = dict.consumer_describe
        that.consumer_form.id = dict.id
        that.is_update = true
        that.addDialogVisible1 = true;
        }
      
    },
    updateComsumerGroup:function(){
        let that = this;
        that.axios.patch("/kops/consumergroup/"+that.consumer_form.id+"/",that.consumer_form).then(res=>{

            if (res.data.code === 200) {
              
                that.$message({
                  message: "修改成功",
                  type: "success",
                  duration: 1500
                });
               that.resetForm1();
                that.load_data(); 
              } else if (res.data.code === 302) {
                that.$message({
                  message: res.data.message,
                  type: "error",
                  duration: 2000
                });
              }  else {
                that.$message({
                  message: "申请发送失败",
                  type: "error",
                  duration: 2000
                });
              }
         
        })
    },
    addComsumerGroup: function() {
        this.$refs["dialog_f1"].validate(valid => {
          if (valid) {
            this.axios
              .post("/kops/consumergroup/", this.consumer_form)
              .then(res => {
                  console.log(res)
                if (res.data.code === 200) {
                  this.addDialogVisible1 = false;
                  this.init();
                  this.resetForm1();
                  this.$message({
                    message: "创建成功",
                    type: "success",
                    duration: 2000
                  });
                } else if (res.data.code === 302) {
                  this.$message({
                    message: res.data.message,
                    type: "error",
                    duration: 2000
                  });
                } else {
                  this.$message({
                    message: "申请发送失败,请输入有效数据",
                    type: "error",
                    duration: 2000
                  });
                }
              });
          }
        });
    },
    resetForm1:function() {
      this.$refs["dialog_f1"].resetFields();
      this.addDialogVisible1 = false;
    },
    deleteconsumer: function(comsume,id,index) {
        let that =this;
        that.$confirm('此操作将永久删除该comsume: '+comsume+', 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
            that.axios.delete('/kops/consumergroup/'+id+'/').then(res=>{
                      if (res.data.code === 200) {
                  this.$message({
                    message: "删除成功",
                    type: "success",
                    duration: 2000
                  });
                  console.log("******",index)
                  this.init();
                } else if (res.data.code === 302) {
                  this.$message({
                    message: res.data.message,
                    type: "error",
                    duration: 2000
                  });
                } else {
                  this.$message({
                    message: "删除失败",
                    type: "error",
                    duration: 2000
                  });
                }

            })
          
        }).catch(() => {
          that.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
     
    },
  }, 
  
  
};
</script>

<style>
.el-table .cell {
  white-space: pre-line;
}
.lag-color{
  color: #CA3536;
}
 .el-table .success-row {
    background: rgb(43, 209, 221);
  }
</style>

