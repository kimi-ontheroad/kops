<template>
<div>
      <el-row type="flex" class="row-bg" justify="center" style="margin-top:10%">
  <el-col :span="6" style="font-size:30px;font-weight:bold;">kafka 管理平台</el-col>
</el-row>
    <el-form :model="form">
    <el-row type="flex"  justify="center" style="margin-top:40px;">
  <el-col :span="6"><el-form-item>
 <el-input placeholder="请输入账号" v-model="form.username"></el-input></el-form-item></el-col>
</el-row>
<el-row type="flex" class="row-bg" justify="center">
  <el-col :span="6"><el-form-item><el-input placeholder="请输入密码" v-model="form.password" show-password></el-input></el-form-item></el-col>
 
</el-row>
<el-row type="flex" class="row-bg" justify="center">
  <el-col :span="6"><el-form-item><el-button style="width:100%" type="primary" @click="login">登录或注册</el-button></el-form-item></el-col>
</el-row>
    </el-form>


</div>
</template>

<script>
export default {
data() {
    return {

        form:{
            username:"",
            password:"",
        }
    }},
    methods:{
        login:function(){
            let that = this;
            that.axios.post("/kops/login", that.form).then(res => {
                console.log(res)
                if (res.data.code === 200) {
                that.$message({
                  message: "登录成功",
                  type: "success",
                  duration: 1500
                });
                let expires = res.data['expires_in'] + 's'
                that.$cookie.set('Authorization', res.data['kafkaid'], {expires});
                that.$cookie.set('username',that.form.username,{expires})
                this.$router.push('/topic')
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

        }
    }
}
</script>

<style>

</style>
