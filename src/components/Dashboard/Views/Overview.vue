<template>
  <div>
    <div class="card" v-for="controller in controllers">
      <table  style="width: 100%">
        <tr>
          <td>
            <div class="header" >
              <h4 class="title">{{controller.description}}</h4>
              <p class="category">{{controller.mac}}</p>
            </div>
          </td>

          <td style="float: right">
            <div class="header text-info" >
              <h2 style="float: right" class="title"><span style="font-size: 16pt">Probability:</span> <span :class="controller.color">{{controller.probability}}%</span></h2>
            </div>
          </td>
        </tr>
      </table>
      <div class="content">
        <div class="row">
          <div class="col-lg-3 col-sm-6" v-for="port in controller.ports">
            <stats-card style ='cursor: pointer;' v-bind:class="{active: port.isActive}" v-on:click.native="select(controller, port)">
              <div class="icon-big text-left icon-warning" slot="header">
                <i :class="port.icon"></i>
              </div>

              <div class="numbers" slot="content">
                <p>{{port.description}}</p>
                {{port.value}}{{port.measure}}
              </div>

              <div class="stats" slot="footer">
                asdsad
                <i class="ti-reload"></i> Updated now
              </div>

            </stats-card>
          </div>

          <div class="col-xs-12">
            <chart-card :chart-data="controller.current_port.data" :chart-options="controller.current_port.options">
              <h4 class="title" slot="title">{{controller.current_port.description}}</h4>
              <span slot="subTitle">{{controller.current_port.type}}</span>
            </chart-card>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import StatsCard from 'components/UIComponents/Cards/StatsCard.vue'
  import ChartCard from 'components/UIComponents/Cards/ChartCard.vue'
  export default {
    components: {
      StatsCard,
      ChartCard,
      'bootstrap-modal': require('vue2-bootstrap-modal')
    },
    /**
     * Chart data used to render stats, charts. Should be replaced with server data
     */
    data () {
      return {
        controllers: [],
        currentPorts: {}
      }
    },
    methods: {
      select: function (controller, port) {
        // console.log(controller)
        for (let i = 0; i < controller.ports.length; ++i) {
          controller.ports[i].isActive = false
        }
        port.isActive = true
        controller.current_port = port
        // this.currentPorts[controller.mac] = port
      },
      listener: function () {
        // let p = 300
        this.axios.get(
          `http://10.0.1.99:8000/api/getControllers/1`)
          .then((response) => {
            for (let i = 0; i < response.data.controllers.length; ++i) {
              for (let j = 0; j < this.controllers.length; ++j) {
                console.log(response.data.controllers[i])
                if (response.data.controllers[i].mac === this.controllers[j].mac) {
                  response.data.controllers[i].current_port = this.controllers[j].current_port
                  console.log(response.data.controllers[i].mac)
                }
              }
            }
            this.controllers = response.data.controllers
          }).catch((err) => {
            console.log(err)
          })
        setInterval(function () {
          this.axios.get(
            `http://10.0.1.99:8000/api/getControllers/1`)
            .then((response) => {
              this.controllers = response.data.controllers
            }).catch((err) => {
              console.log(err)
            })
        }.bind(this), 5000)
      }
    },
    mounted: function () {
      // this.currentCard = this.statsCards[0]
      this.listener()
    }
  }

</script>
<style>

</style>
