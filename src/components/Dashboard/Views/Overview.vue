<template>
  <div>
    <div class="row">
      <div class="col-lg-3 col-xs-6" style="cursor: pointer">
        <div class="card" v-on:click="myFilter">

          <div class="content" style="text-align: center; padding-top: 50px; padding-bottom: 50px">
            <i class="ti-plus" style="font-size: 25pt"></i>
          </div>
        </div>
      </div>
    </div>
    <div class="card">
      <table  style="width: 100%">
        <tr>
          <td>
            <div class="header" >
              <h4 class="title">Diesel generator #1</h4>
              <p class="category">E8:1C:8D:11:22:88</p>
            </div>
          </td>

          <td style="float: right">
            <div class="header text-info" >
              <h2 style="float: right" class="title"><span style="font-size: 16pt">Probability:</span> <span class="text-danger">94%</span></h2>
            </div>
          </td>
        </tr>
      </table>

      <div class="content">
        <div class="row">
          <div class="col-lg-3 col-sm-6" v-for="stats in statsCards">
            <stats-card style ='cursor: pointer' v-bind:class="{ active: stats.isActive }"  v-on:click.native="test(stats)">

              <div class="icon-big text-left" :class="`icon-${stats.type}`" slot="header">
                <i :class="stats.icon"></i>
              </div>
              <div class="numbers" slot="content" >
                <p>{{stats.title}}</p>
                {{stats.value}}
              </div>
              <div class="stats" slot="footer">
                <i :class="stats.footerIcon"></i> {{stats.footerText}}
              </div>
            </stats-card>
          </div>

          <div class="col-xs-12">
            <chart-card :id="currentCard.id" :chart-data="currentCard.usersChart.data" :chart-options="currentCard.usersChart.options">
              <h4 class="title" slot="title">{{currentCard.title}}</h4>
              <span slot="subTitle">{{currentCard.footerText}}</span>

            </chart-card>
          </div>

        </div>



      </div>
    </div>


    <div class="card">
      <div class="header">
        <h4 class="title">Diesel generator #2</h4>
        <p class="category">E8:1C:8D:11:22:88</p>
      </div>
      <div class="content">
        <div class="row">
          <div class="col-lg-3 col-sm-6" v-for="stats in statsCards">
            <stats-card style ='cursor: pointer' v-bind:class="{ active: stats.isActive }"  v-on:click.native="test(stats)">

              <div class="icon-big text-left" :class="`icon-${stats.type}`" slot="header">
                <i :class="stats.icon"></i>
              </div>
              <div class="numbers" slot="content" >
                <p>{{stats.title}}</p>
                {{stats.value}}
              </div>
              <div class="stats" slot="footer">
                <i :class="stats.footerIcon"></i> {{stats.footerText}}
              </div>
            </stats-card>
          </div>

          <div class="col-xs-12">
            <chart-card :id="currentCard.id" :chart-data="currentCard.usersChart.data" :chart-options="currentCard.usersChart.options">
              <h4 class="title" slot="title">{{currentCard.title}}</h4>
              <span slot="subTitle">{{currentCard.footerText}}</span>

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
      ChartCard
    },
    /**
     * Chart data used to render stats, charts. Should be replaced with server data
     */
    data () {
      return {
        currentCard: {
          id: 'plot0',
          type: 'warning',
          icon: 'ti-crown',
          title: 'Темр',
          value: '105GB',
          footerText: 'Updated now',
          footerIcon: 'ti-reload',
          isActive: true,
          usersChart: {
            data: {
              labels: [], // ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
              series: [
                [23, 113, 67, 108, 190, 239, 307, 410, 410]
              ]
            },
            options: {
              seriesBarDistance: 10,
              axisX: {
                showGrid: false
              },
              height: '245px'
            }
          }
        },
        statsCards: [
          {
            id: 'plot0',
            type: 'warning',
            icon: 'ti-crown',
            title: 'Intake sensor #1',
            value: '105GB',
            footerText: 'Temp sensor',
            footerIcon: 'ti-reload',
            isActive: true,
            usersChart: {
              data: {
                labels: [], // ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
                series: [
                  [23, 113, 67, 108, 190, 239, 307, 410, 410]
                ]
              },
              options: {
                seriesBarDistance: 10,
                axisX: {
                  showGrid: false
                },
                height: '245px'
              }
            }
          },
          {
            id: 'plot1',
            type: 'success',
            icon: 'ti-crown',
            title: 'Temp sensors',
            value: '$1,345',
            footerText: 'Last day',
            footerIcon: 'ti-calendar',
            isActive: false,
            usersChart: {
              data: {
                labels: [], // ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
                series: [
                  [23, 113, 67, 108, 190, 239, 307, 410, 410]
                ]
              },
              options: {
                seriesBarDistance: 10,
                axisX: {
                  showGrid: false
                },
                height: '245px'
              }
            }
          },
          {
            id: 'plot2',
            type: 'danger',
            icon: 'ti-pulse',
            title: 'Vibration',
            value: '23',
            footerText: 'Main rotor ',
            footerIcon: 'ti-timer',
            isActive: false,
            usersChart: {
              data: {
                labels: [], // ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
                series: [
                  [23, 113, 67, 108, 190, 239, 307, 410, 410]
                ]
              },
              options: {
                seriesBarDistance: 10,
                axisX: {
                  showGrid: false
                },
                height: '245px'
              }
            }
          },
          {
            id: 'plot3',
            type: 'info',
            icon: 'ti-twitter-alt',
            title: 'Followers',
            value: '+45',
            footerText: 'Updated now',
            footerIcon: 'ti-reload',
            isActive: false,
            usersChart: {
              data: {
                labels: [], // ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
                series: [
                  [23, 113, 67, 108, 190, 239, 307, 410, 410]
                ]
              },
              options: {
                seriesBarDistance: 10,
                axisX: {
                  showGrid: false
                },
                height: '245px'
              }
            }
          },
          {
            id: 'plot4',
            type: 'info',
            icon: 'ti-twitter-alt',
            title: 'Followers',
            value: '+45',
            footerText: 'Updated now',
            footerIcon: 'ti-reload',
            isActive: false,
            usersChart: {
              data: {
                labels: [], // ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
                series: [
                  [23, 113, 67, 108, 190, 239, 307, 410, 410]
                ]
              },
              options: {
                seriesBarDistance: 10,
                axisX: {
                  showGrid: false
                },
                height: '245px'
              }
            }
          }
        ],
        usersChart: {
          data: {
            labels: [], // ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
            series: [
              [13, 313, 67, 108, 190, 739, 307, 410, 410]
            ]
          },
          options: {
            seriesBarDistance: 10,
            axisX: {
              showGrid: false
            },
            height: '245px'
          }
        },
        activityChart: {
          data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            series: [
              [542, 543, 520, 680, 653, 753, 326, 434, 568, 610, 756, 895],
              [230, 293, 380, 480, 503, 553, 600, 664, 698, 710, 736, 795]
            ]
          },
          options: {
            seriesBarDistance: 10,
            axisX: {
              showGrid: false
            },
            height: '245px'
          }
        },
        preferencesChart: {
          data: {
            labels: ['62%', '32%', '6%'],
            series: [62, 32, 6]
          },
          options: {}
        }

      }
    },
    methods: {
      test: function (_this) {
        // alert('1')
        // this.addClass('alert').addClass('alert-info')
        console.log(_this)
        for (let i = 0; i < this.statsCards.length; ++i) {
          this.statsCards[i].isActive = false
        }
        _this.isActive = true
        this.currentCard = _this
      },
      listener: function () {
        let p = 300
        let loop = function () {
          for (let i = 0; i < this.statsCards.length; ++i) {
            this.statsCards[i].usersChart.data.series[0].push(p)
            this.statsCards[i].value = `${p}GB`
            // let a = document.getElementById(`plot${this.currentCard.id}`)
            // console.log(a)
            // console.log(this.currentCard)
            // console.log($(`#plot${this.statsCards[i].id}`))
            p += (50 * Math.floor(Math.random() * 9) - 9)
            // console.log(p)
          }
          // console.log(this.statsCards[0].usersChart.data.series[0].length)
          // lconsole.log(this.statsCards[1].usersChart.data.series[0].length)
        }

        setInterval(loop.bind(this), 5000)
      },
      myFilter: function () {
        console.log(this)
      }
    },
    mounted: function () {
      this.currentCard = this.statsCards[0]
      this.listener()
    }
  }

</script>
<style>

</style>
