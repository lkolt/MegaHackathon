<template>
  <div class="card">
    <div class="header">
      <h4 class="title">New controller</h4>
    </div>
    <div class="content">
      <form>
        <div class="row">
          <div class="col-md-6">
            <fg-input type="text"
                      label="MAC"
                      :disabled="false"
                      placeholder="Type MAC of your IoT controller"
                      v-model="mac">
            </fg-input>
          </div>
        </div>
        <div class="text-right">
          <button type="submit"  l="buttonText" class="btn btn-info btn-fill btn-lg" @click.prevent="checkMac">
            {{macButtonText}}
          </button>
        </div>
        <hr>
        <div class="row">
          <h5 class="content" v-if="showSetText">Set ports</h5>
          <div>
            <div v-if="showSetText"  class="col-xs-6" >
              <fg-input type="text"
                        label="Type description of your IoT controller"
                        :disabled="false"
                        :placeholder="description"
                        v-model="description"
              >
              </fg-input>
            </div>
          </div>
          <div class="clearfix"></div>
          <div v-for="port in ports">
            <div class="col-xs-2" >
              <fg-input type="text"
                        label="Type"
                        :disabled="true"
                        :placeholder="port.type"
                        v-model="port.type"
              >
              </fg-input>
            </div>
            <div class="col-xs-6" >
              <fg-input type="text"
                        label="Description"
                        :disabled="false"
                        :placeholder="port.description"
                        v-model="port.description"
              >
              </fg-input>
            </div>
            <div class="col-xs-1" >
              <fg-input type="text"
                        label="Min"
                        :disabled="false"
                        :placeholder="port.min_value"
                        v-model="port.min_value"
              >
              </fg-input>
            </div>
            <div class="col-xs-1" >
              <fg-input type="text"
                        label="Max"
                        :disabled="false"
                        :placeholder="port.max_value"
                        v-model="port.max_value"
              >
              </fg-input>
            </div>

            <div class="col-xs-2" >
              <fg-input type="text"
                        label="Measurem."
                        :disabled="true"
                        :placeholder="port.measurement"
                        v-model="port.measurement"
              >
              </fg-input>
            </div>
            <div class="clearfix"></div>
          </div>
        </div>
        <div class="text-center">
          <button type="submit" v-if="setButtonVisible"  l="buttonText" class="btn btn-info btn-fill btn-wd" @click.prevent="sendPorts">
            {{setButtonText}}
          </button>
        </div>



      </form>
    </div>
  </div>
</template>
<script>
  import PaperNotification from 'src/components/UIComponents/NotificationPlugin/Notification.vue'
  export default {
    data () {
      return {
        mac: '',
        description: '',
        macButtonText: 'Check availability',
        setButtonText: 'Set ports',
        setButtonVisible: false,
        showSetText: false,
        ports: []
      }
    },
    components: {
      PaperNotification
    },
    methods: {
      checkMac () {
        let mac = this.mac
        if (mac === '') {
          this.notifyVue('Empty MAC, for continue type MAC of your controller', 'danger')
          return
        }
        this.macButtonText = 'Loading...'
        this.axios.get(`http://10.0.1.99:8000/api/checkMac/${mac}`, {
          withCredentials: false
        }).then((response) => {
          if (response.data.status === 'error' && response.data.message === '') {
            this.notifyVue('Current MAC already used or not exist', 'warning')
          } else if (response.data.status === 'ok' && response.data.message !== '') {
            this.ports = response.data.message
            this.setButtonVisible = true
            this.showSetText = true
          }
          this.macButtonText = 'Check availability'
          console.log(response.data)
        }).catch((err) => {
          this.macButtonText = 'Check availability'
          this.notifyVue('Some error, try again later', 'danger')
          console.log(err)
        })
      },
      sendPorts: function () {
        let _ports = []
        for (let i = 0; i < this.ports.length; ++i) {
          console.log(this.ports[i])
          if (!this.description || !this.ports[i].id || !this.ports[i].type || !this.ports[i].description || !this.ports[i].min_value || !this.ports[i].max_value || !this.ports[i].measurement) {
            this.notifyVue('Not all ports has been set', 'danger')
            return
          }
          _ports.push({
            id: this.ports[i].id,
            type: this.ports[i].type,
            description: this.ports[i].description,
            min_value: this.ports[i].min_value,
            max_value: this.ports[i].max_value,
            measurement: this.ports[i].measurement
          })
        }
        this.setButtonText = 'Loading...'
        let data = JSON.stringify({
          description: this.description,
          mac: this.mac,
          ports: _ports
        })
        this.axios.post(
          `http://10.0.1.99:8000/api/setPorts`, data, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
          }).then((response) => {
            if (response.data.status === 'error' && response.data.message !== '') {
              this.notifyVue(response.data.message, 'warning')
            } else if (response.data.status === 'ok' && response.data.message === '') {
              this.mac = ''
              this.ports = []
              this.showSetText = false
              this.setButtonVisible = false
              this.notifyVue('Ports has been set successfully', 'success')
            }
            this.setButtonText = 'Set ports'
          }).catch((err) => {
            this.setButtonText = 'Set ports'
            console.log(err)
          })
      },
      notifyVue (body, color) {
        this.$notifications.notify(
          {
            message: body,
            icon: 'ti-bell',
            horizontalAlign: 'right',
            verticalAlign: 'bottom',
            type: color
          })
      }
    }
  }

</script>
<style>

</style>
