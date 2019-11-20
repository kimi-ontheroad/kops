
<template>
<div>
    <el-row type="flex" class="row-bg" justify="center">
  <el-col :span="4"> <el-button
              @click="form.id='',form.is_update=false,addDialogVisible=true"
              type="primary"
              style="font-size: 16px;padding: 11px"
            >新建Topic</el-button></el-col>
  <el-col :span="6"></el-col>
  <el-col :span="10">
      <el-row :gutter="20">
  <el-col :span="16"><el-input
                @keyup.enter.native="search"
                v-model="topic_filter"
                placeholder="请输入Topic"
                prefix-icon="el-icon-search"
                clearable
                @clear="load_data"
              ></el-input></el-col>
  <el-col :span="8"> <el-button
                type="primary"
                @click="search"
                style="padding: 11px;
  font-size: 16px;"
              >确 定</el-button></el-col>
</el-row>
     </el-col>
</el-row>
<el-table :data="table_data" style="padding:30px 30px 0 30px;margin-top:20px" :header-cell-style="{background:'#e5e9f2'}">
          
        <el-table-column label="Topic名称" min-width="8" width="261" align="center" show-overflow-tooltip>
          <template slot-scope="scope">
            <div>
              {{scope.row.topic_name}}
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="cluster" label="所属kafka集群" min-width="12" align="center"></el-table-column>

        <el-table-column prop="partition" label="Partition" min-width="6" align="center"></el-table-column>

        <el-table-column prop="create_user" label="申请人" min-width="7" align="center"></el-table-column>

        <el-table-column label="生产Broker List" width="270" align="center">
          <template slot-scope="scope">
               <div v-if="scope.row.brokers">
              <div v-for="broker in scope.row.brokers.split(',')">{{broker}}</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="操作" min-width="12" align="center">
          <template slot-scope="scope">
            <div style="margin-bottom: 4px">
              <el-button
                type="success"
                style="padding: 5px 16px;font-size: 13px"
                @click="updateTopic(scope.row.id, scope.row.index)"
              >Topic管理</el-button>
            </div>

            <div style="margin-bottom: 4px">
              <el-button
                type="success"
                style="padding: 5px 16px;font-size: 13px"
                :disabled="scope.row.status ===0"
                @click="kafka_consume(scope.row.id,scope.row.cluster,scope.row.partition, scope.row.topic_name,scope.row.brokers)"
              >消费管理</el-button>
            </div>
           
              <el-button
                type="success"
                style="padding: 5px 16px;font-size: 13px"
                @click="goTopicMonitor(scope.row.topic_name,scope.row.cluster,scope.row.status,scope.row.id,scope.row.brokers)"
              >报警管理</el-button>
          </template>
        </el-table-column>
      </el-table>

 <div>
      <el-dialog
        :title="form.is_update?(form.status?'Kafka Topic':'修改 Kafka Topic'):'申请 Kafka Topic'"
        :visible.sync="addDialogVisible"
        @close="resetForm()"
      >
        <hr style="margin: -20px 0 25px 0">
        <el-form :model="form" :rules="rules" ref="dialog_f" v-loading="form_loading">
          <el-row>
            <el-col :span="20">
              <el-form-item prop="topic_name" :label-width="leftWidth">
                <el-input
                  v-model="form.topic_name"
                  placeholder="Topic名称"
                  :disabled="form.status===1"
                ></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="10">
              <el-form-item :label-width="leftWidth" prop="cluster">
                <el-select
                  v-model="form.cluster"
                  placeholder="申请kafka集群名称"
                  style="width: 100%"
                >
                  <el-option v-for="key,value in clusters" :label="key" :value="value" :key="value"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="10">
              <el-form-item :label-width="leftWidth" prop="service_name">
                <el-input
                  v-model="form.service_name"
                  placeholder="日志所属服务名称"
                  :disabled="form.status===1"
                  style="width:100%"
                ></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="10">
              <el-form-item :label-width="leftWidth" prop="kafka_client">
                <el-select
                  clearable
                  multiple
                  placeholder="生产客户端"
                  :disabled="form.status===1"
                  v-model="form.kafka_client"
                  style="width: 100%"
                >
                  <el-option v-for="item in kafka_client" :label="item" :value="item" :key="item"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item prop="peak_volume" :label-width="rightWidth">
                <el-input
                  v-model="form.peak_volume"
                  placeholder="高峰QPS"
                  :disabled="form.is_update"
                  style="width: 100%"
                ></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <div style="margin: 10px 0 0 10px">条/秒</div>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="10">
              <el-form-item :label-width="leftWidth" prop="machine_number">
                <el-input
                  v-model="form.machine_number"
                  placeholder="生产机器数量"
                  :disabled="form.status===1"
                  style="width: 100%"
                ></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item prop="size_per_log" :label-width="rightWidth">
                <el-input
                  v-model="form.size_per_log"
                  placeholder="单条日志大小"
                  :disabled="form.is_update"
                  style="width: 100%"
                ></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <div style="margin: 10px 0 0 10px">kB</div>
            </el-col>
          </el-row>
          <el-form-item prop="describe">
            <el-input
              v-model="form.describe"
              placeholder="日志用途描述"
              :disabled="form.status===1"
              style="width:92%"
            ></el-input>
          </el-form-item>
          <el-form-item  style="margin-right:-10px;" prop="machine_ip">
            <el-input
              type="textarea"
              v-model="form.machine_ip"
              :disabled="form.status===1"
              placeholder="生产机器IP列表"
              :rows="6"
              style="width: 92%"
            ></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button v-if="!(form.is_update)"
            type="success"
            @click="addTopic" 
          >创建</el-button>
          <el-button v-else
            type="success"
            @click="commitTopic" 
          >修改</el-button>
          <el-button type="danger" v-if="form.is_update" @click="deleteTopic(form.topic_name,form.index)">删除</el-button>
          <el-button @click="resetForm(),addDialogVisible = false">取 消</el-button>
        </div>
      </el-dialog>
    </div>
    <!-- 申请消费弹出框 -->
    <div>
      <el-dialog title="申请消费kafka的Groupid" :visible.sync="addDialogVisible1" @close="resetForm()">
        <hr style="margin: -20px 0 25px 0">
        <el-form :model="consumer_form" :rules="rules1" ref="dialog_f1" v-loading="form_loading">
          <el-form-item prop="consumer_group_name" label="申请消费group名称" label-width="160px">
            <el-col :span="8">
              <el-input v-model="consumer_form.consumer_group_name"></el-input>
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
          <el-button
            type="success"
            @click="addComsumerGroup"
          >确 定</el-button>
          <el-button @click="resetForm1()">取 消</el-button>
        </div>
      </el-dialog>
    </div>
  



</div>
</template>

<script>
export default {
  data() {
    return {
    user_name:"",
    topicid:0,
      clusters: {
        "center":"中心集群"
      },
      status: {
        0: "未上线",
        1: "已上线"
      },
      color: {
        0: "status_off",
        1: "status_on"
      },
      consumer_status: 0,
      kafka_client: ["Go", "Python", "C++", "Java", "Filebeat", "Flink", "Lua"],
      form: {
        cluster: "",
        service_name: "",
        describe: "",
        topic_name: "",
        size_per_log: "",
        peak_volume: "",
        kafka_client: [],
        machine_number: "",
        machine_ip: "",
        create_user: this.$cookie.get("username"),
        is_update: false,
        id: "",
      },
      form_loading: false,
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
      rules: {
        product: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        service_name: [
          { required: true, message: "该项不能为空", trigger: "change" }
        ],
        describe: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        topic_name: [
          { required: true, message: "该项不能为空", trigger: "change" }
        ],
        volume: [
          { required: true, message: "该项不能为空", trigger: "change" }
        ],
        unit: [{ required: true, message: "该项不能为空", trigger: "blur" }],
        size_per_log: [
          { required: true, message: "该项不能为空", trigger: "change" }
        ],
        peak_volume: [
          { required: true, message: "该项不能为空", trigger: "change" }
        ],
        kafka_client: [
          { required: true, message: "该项不能为空", trigger: "blur" }
        ],
        machine_number: [
          { required: true, message: "该项不能为空", trigger: "change" }
        ],
        machine_ip: [
          { required: true, message: "该项不能为空", trigger: "change" }
        ],
        cluster: [
          {
            required: true,
            message: "该项不能为空",
            trigger: "change"
          }
        ]
      },
      //申请消费groupID表单验证规则
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

      current_content: "topic",

      table_data: [],
      empty_text: "请输入Group Id",

      addDialogVisible: false,
      addDialogVisible1: false,
      current_page: 1,
      total: 10,
      size: 10,

      topic_filter: "",

      leftWidth: "20px",
      rightWidth: "80px"
    };
  },
  mounted: function() {
    this.load_data();
  },

  beforeDestroy() {
  },

  methods: {
    load_data: function() {
      let that = this;
      that.axios
        .get("/kops/topics/", {
          params: {
            topic_name: this.topic_filter,
            create_user:this.user_name
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
          that.table_data = _data;
          
        });
    },
    commitTopic:function(){
        let that = this;
        console.log('hdjshdjshdjs')
        this.$refs["dialog_f"].validate(valid => {
          if (valid) {
            this.form_loading = true;
            this.axios.patch("/kops/topics/"+that.topicid+"/", that.form).then(res => {
              that.form_loading = false;
              if (res.data.code === 200) {
                that.addDialogVisible = false;
                that.$message({
                  message: "修改成功",
                  type: "success",
                  duration: 1500
                });
               that.form.is_update = false;
                that.resetForm();
                that.load_data();

              } else if (res.data.code === 302) {
                that.$message({
                  message: res.data.message,
                  type: "error",
                  duration: 2000
                });
              }  else {
                that.$message({
                  message: "修改发送失败",
                  type: "error",
                  duration: 2000
                });
              }
            });
          } else {
            return false;
          }
        });
  
             
            
    },

    addTopic: function() {
      let that = this;
        this.$refs["dialog_f"].validate(valid => {
          if (valid) {
            this.form_loading = true;
            this.axios.post("/kops/topics/", that.form).then(res => {
              that.form_loading = false;
              that.form.is_update = false;
              if (res.data.code === 200) {
                that.addDialogVisible = false;
                that.$message({
                  message: "创建成功",
                  type: "success",
                  duration: 1500
                });
                that.load_data();
                that.resetForm();
              } else if (res.data.code === 302) {
                that.$message({
                  message: res.data.message,
                  type: "error",
                  duration: 2000
                });
              }  else {
                that.$message({
                  message: "创建发送失败",
                  type: "error",
                  duration: 2000
                });
              }
            });
          } else {
            return false;
          }
        });
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
                  this.resetForm1();
                  this.$message({
                    message: "申请发送成功",
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
    updateTopic: function(id,index) {
      let that = this;
      this.addDialogVisible = true;
      this.form.is_update = true;
        this.axios
          .get("/kops/topics/", {
            params: {
              id: id
            }
          })
          .then(res => {
              console.log(res)
            if (res.data) {
              let data = res.data[0].fields;
              that.form.service_name = data.service_name;
              that.form.describe = data.describe;
              that.form.topic_name = data.topic_name;
              that.form.topic_volume = data.topic_volume;
              that.form.size_per_log = data.size_per_log;
              that.form.partition = data.partition
          that.form.peak_volume = data.peak_volume;
          that.form.generate_principle = data.generate_principle;
          that.form.kafka_client = data.kafka_client.split(",");
          that.form.machine_number = data.machine_number;
          that.form.machine_ip = data.machine_ip;
          that.form.create_user = data.create_user
          that.form.is_update = true;
          that.form.id = data.id;
          that.topicid = id
          that.form.status = data.status;
          that.form.cluster = data.cluster;
          that.form['index']=index;
        }
      });
    },
    applycomsume: function(topic_name, cluster, status, topicid, brokerlist) {
      let that = this;
        that.consumer_form.consumer_cluster = cluster;
        that.consumer_form.consumer_topic = topicid;
        that.consumer_form.topic_name = topic_name;
        that.consumer_form.topic_id = topicid;
        that.consumer_form.consumer_broker_list = brokerlist;
        that.consumer_form.consumer_user = "this.user_name"
        that.addDialogVisible1 = true;
        console.log(topic_name, cluster, status, topicid, brokerlist)
      
    },

    handleCurrentChange(val) {
      this.current_page = val;
      this.load_data();
    },

    resetForm() {
      this.$refs["dialog_f"].resetFields();
    },
    resetForm1() {
      this.$refs["dialog_f1"].resetFields();
      this.addDialogVisible1 = false;
    },

    is_disabled: function(cluster) {
      return (
        cluster === "ad_kafka" ||
        cluster === "dc_kafka" ||
        cluster === "kafka-0.10.0.1"
      );
    },

    search: function() {
      this.current_page = 1;
      this.load_data();
    },

    deleteTopic: function(topic, index) {
        let that =this;
        that.$confirm('此操作将永久删除该topic: '+topic+', 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
            that.axios.delete('/kops/topics/'+topic+'/').then(res=>{
                      if (res.data.code === 200) {
                  this.$message({
                    message: "删除成功",
                    type: "success",
                    duration: 2000
                  });
                  this.load_data();
                  this.addDialogVisible = false;
                  delete this.form.index
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
    goTopicMonitor:function(topic, cluster, partition,topic_name,a){
         this.$router.push(
          "/monitor/?topic=" +
            topic +
            "&cluster=" +
            cluster +"&partition="+partition+"&topic_name="+topic_name+"&brokers="+a
        );

    },

    kafka_consume: function(topic, cluster, partition,topic_name,a) {
        this.$router.push(
          "/comsume/?topic=" +
            topic +
            "&cluster=" +
            cluster +"&partition="+partition+"&topic_name="+topic_name+"&brokers="+a
        );
      sessionStorage.setItem("topic", topic);
      sessionStorage.setItem("cluster", cluster);
    },
    redirect: function() {
    }
  }
};
</script>

<style>
.el-table .cell {
  white-space: pre-line;
}
.status_on {
  background-color: #00b609;
  color: #fff;
}
.status_off {
  background-color: #ff0000;
  color: #fff;
}
.el-button {
  padding: 12px 12px;
  font-size: 14px;
}
.el-input__inner {
  width: 100%;
}
</style>
