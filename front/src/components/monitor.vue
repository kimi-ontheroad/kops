
<template>
<div>
    <el-row type="flex" class="row-bg" justify="center">
  <el-col :span="4"> <el-button
              @click="get_groups(false)"
              type="primary"
              style="font-size: 16px;padding: 11px"
            >新建报警</el-button></el-col>
  <el-col :span="6"></el-col>
  <el-col :span="10">
      <el-row :gutter="20">
  <el-col :span="16"><el-input
                @keyup.enter.native="search"
                v-model="topic_filter"
                placeholder="请输入消费名称"
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
<el-table :data="table_data" style="padding:30px 30px 0 30px;margin-top:30px;" :header-cell-style="{background:'#e5e9f2'}">
          
        <el-table-column label="Consume名称" min-width="8" width="261" align="center" show-overflow-tooltip>
          <template slot-scope="scope">
            <!-- <div  @click="updateTopic(scope.row.id)"
                  style="white-space: normal;width: 250px; cursor: pointer; color: #409eff;"> -->
              {{scope.row.group__consumer_group_name}}
            <!-- </div> -->
          </template>
        </el-table-column>

        <el-table-column prop="value" label="阀值" min-width="6" align="center"></el-table-column>

        <el-table-column prop="creator" label="申请人" min-width="6" align="center"></el-table-column>

        <el-table-column prop="cc_list" label="报警接收人" min-width="7" align="center"></el-table-column>

        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
                  <el-button type="success" v-if="scope.row.status" style="font-size: 1em; padding: 8px;width:100%;" @click="changestatus(false,scope.row.id)">运行</el-button>
                  <el-button type="danger" v-else style="font-size: 1em; padding: 8px;width:100%;" @click="changestatus(true,scope.row.id)">暂停</el-button>
          </template>
        </el-table-column>

        <el-table-column label="操作" min-width="12" align="center">
          <template slot-scope="scope">
              <div style="margin-bottom: 4px">
              <el-button
                type="success"
                style="padding: 5px 16px;font-size: 13px"
                @click="updateMonitor(scope.row)"
              >编辑报警</el-button>
            </div>
            <div style="margin-bottom: 4px">
              <el-button
                type="success"
                style="padding: 5px 16px;font-size: 13px"
                @click="deletemonitor(scope.row.group__consumer_group_name,scope.row.id)"
              >删除报警</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
<el-dialog 
        :title="form.is_update?'修改报警':'创建报警'"
:visible.sync="addDialogVisible1" @close="resetForm1()">
        <hr style="margin: -20px 0 25px 0">
        <el-form :model="form" :rules="rules1" ref="dialog_f1" v-loading="form_loading">
          <el-form-item prop="group" label="选择消费group" label-width="160px">
            <el-col :span="8">
              <el-select v-model="form.group">
                <el-option v-for="item in groups" :label="item" :value="item" :key="item"></el-option>
              </el-select>
            </el-col>
          </el-form-item>
          <el-form-item prop="value" label="阀值" label-width="160px">
            <el-col :span="20">
              <el-input v-model="form.value"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="cc_list" label="报警接收人" label-width="160px">
            <el-col :span="12">
              <el-input
                v-model="form.cc_list"
                placeholder="报警接收人"
              ></el-input>
            </el-col>
          </el-form-item>
          <el-form-item prop="creator" label="申请人" label-width="160px">
            <el-col :span="12">
              <el-input
                v-model="form.creator"
                placeholder="申请人"
                disabled
              ></el-input>
            </el-col>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            {{form.is_update}}
          <el-button v-if="!(form.is_update)"
            type="success"
            @click="addMonitor"
          >确 定</el-button>
           <el-button v-else
            type="success"
            @click="commitMonitor"
          >确定</el-button>
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
        status: {
        0:'暂停',
        1:'运行',
      },
       color: {
        0: "status_off",
        1: "status_on",
      },
        form_loading:false,
        topic_filter:"",
        groups:[],
        addDialogVisible1:false,
        table_data:[],
        form:{
            is_update:false,
            topics:"",
            group:"",
            value:"",
            cc_list:"",
            creator:this.$cookie.get("username"),
            status:1,
        },
        rules1:{
             group: [
          {
            required: true,
            message: "该项不能为空",
            trigger: "blur"
          }
        ],
        value: [
          {
            required: true,
            message: "该项不能为空",
            trigger: "blur"
          }
        ],
        cc_list: [
          {
            required: true,
            message: "该项不能为空",
            trigger: "blur"
          }
        ]

        },
      topic_name:"",
      partition:'',
      topic: "",
      cluster: "",
      brokers:"",
    }
    
    },
    mounted: function() {
       this.topic = this.$route.query.topic;
        this.cluster = this.$route.query.cluster;
        this.partition = this.$route.query.partition;
        this.topic_name = this.$route.query.topic_name;
        this.brokers = this.$route.query.brokers;
        this.load_data();
  },
    methods:{
         redirect: function() {
      window.history.go(-1);
    },
        search: function() {
      this.current_page = 1;
      this.load_data();
    },
        deletemonitor: function(name,id) {
        let that =this;
        that.$confirm('此操作将永久删除该报警: '+name+', 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
            that.axios.delete('/kops/monitor/'+id+'/').then(res=>{
                      if (res.data.code === 200) {
                  this.$message({
                    message: "删除成功",
                    type: "success",
                    duration: 2000
                  });
                  this.load_data();
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
    changestatus:function(flag, id){
        let that = this
            this.axios.put("/kops/monitor/"+id+"/", {"status":flag?1:0}).then(res=>{
               if (res.data.code === 200) {
              
                that.$message({
                  message: flag?"运行成功":"暂停成功",
                  type: "success",
                  duration: 1500
                });
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

            })

       
    },

    commitMonitor:function(){

        let that = this;
        console.log('hdjshdjshdjs')
    //   this.form.topic_volume = this.form.volume * this.form.unit;
        this.$refs["dialog_f1"].validate(valid => {
          if (valid) {
            this.form_loading = true;
            this.axios.patch("/kops/monitor/"+this.form.id+"/", that.form).then(res => {
              that.form_loading = false;
              if (res.data.code === 200) {
              
                that.$message({
                  message: "修改成功",
                  type: "success",
                  duration: 1500
                });
               this.form.is_update = false;
               delete this.form.id 
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
        load_data: function() {
      let that = this;
        that.loading = true;
      that.axios
        .get("/kops/monitor/", {
          params: {
            topics: this.topic_name,
            group:this.topic_filter
          }
        })
        .then(res => {
          console.log(res.data);
          let data = res.data.data;

          that.table_data = data;
          console.log(data)
              
          
        });
    },
        
        resetForm1() {
      this.$refs["dialog_f1"].resetFields();
      this.addDialogVisible1 = false;
    },
    get_groups:function(is_update){
        let that = this;
        that.form.is_update=false,
        
        that.axios.get("/kops/consumergroup/",{  params: {
            consumer_topic: this.topic_name,
          }}).then(res=>{
              console.log(res.data)
              let _data = res.data;
        let children = []
        if (_data){
        _data.forEach((item,index)=>{
          children.push(item.fields.consumer_group_name)})
             that.groups = children
             if(!is_update){that.addDialogVisible1=true
              delete that.form.id}
             else{
                 that.form.is_update=true;
                 that.addDialogVisible1=true;
                 
             }
             }

          })

    },
      updateMonitor: function(dict) {
      let that = this;
       console.log(dict)
        that.form.is_update = true;
        that.form.topics = dict.topics__topic_name;
        that.form['id'] = dict.id
        that.form.group = dict.group__consumer_group_name;
        that.form.status = dict.status;
        that.form.topics = that.topic_name;
        that.form.cc_list = dict.cc_list;
        that.form.creator = dict.creator;
        that.form.value = dict.value;
        that.get_groups(true);
        that.addDialogVisible1 = true;
      
    },
    addMonitor:function(){
        this.$refs["dialog_f1"].validate(valid => {
            this.form.topics = this.topic_name
          if (valid) {
            this.axios
              .post("/kops/monitor/", this.form)
              .then(res => {
                  console.log(res)
                if (res.data.code === 200) {
                  
                  this.$message({
                    message: "创建成功",
                    type: "success",
                    duration: 2000
                  });
                  this.resetForm1();
                  this.load_data();
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


    }
    }
}
</script>

<style>
 .status_on {
  background-color: #00b609;
  color: #fff;
}
.status_off {
  background-color: #ff0000;
  color: #fff;
}
 
</style>
