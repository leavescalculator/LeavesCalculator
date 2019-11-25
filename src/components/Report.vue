<template>
  <div id="report" v-if="user.employee_id != null">
    <h1>Portland State University Leave Worksheet</h1>
    <hr />

    <h3>Employee Information</h3>
    <table width="800">
      <tr>
        <td>Employee Name: {{ user.first_name }} {{ user.last_name }}</td>
        <td>Date: {{ new Date().toDateString() }}</td>
      </tr>
      <tr>
        <td>Hire Date: {{ user.hire_date }}</td>
        <td>PSU ID #: {{ user.employee_id }}</td>
      </tr>
      <tr>
        <td>Payrate: {{ 0 }}  </td>
      </tr>
    </table>
    <hr />

    <h3>Eligibility</h3>
    <table width="800">
      <tr>
        <td>Look Back Hours: {{ user.month_lookback_12 }}</td>
        <td>FTE: {{ user.fte }}</td>
      </tr>
      <tr>
        <td>Months: {{ 0 }}</td>
        <td>E-Class: {{ 0 }}</td>
      </tr>
      <tr>
        <td>FMLA: {{ user.fmla_eligibility }}</td>
        <td>OFLA: {{ user.ofla_eligibility }}</td>
      </tr>
      <tr>
        <td>Hours Eligible: {{0}}</td>
        <td>* {{0}}</td>
      </tr>
      <tr>
        <td>Worksite Location: {{0}}  </td>
        <td>Due to a Work Related Injury? {{0}}</td>
      </tr>
    </table>
    <hr />

    <h3>Leave Balance</h3>
    <table width="800">
      <tr>
        <td><b>Total Paid Leave Available: {{ 0 }}</b></td>
        <td><b>Total Leave Request: {{ total_request }} </b></td>
      </tr>
      <tr>
        <td>
          Sick Leave: {{ user.paid_leave_balances['ASIC'] }}
        </td>
        <td>FSLA</td>
        <td>
          Personal Leave: {{ user.paid_leave_balances['PERS'] }}
        </td>
        <td>AAUP DSLB: {{ aaup ? "Yes" : "No" }} </td>
      </tr>
      <tr>
        <td>
          Vacation Leave: {{ user.paid_leave_balances['AVAC'] }}
        </td>
        <td>NSLA</td>
        <td>
          Exchange: {{ user.paid_leave_balances['XCHG'] }}
        </td>
        <td>
          DSLB Total: {{ dslb }}
        </td>
      </tr>
      <tr>
        <td>ST Disability?: {{ lst ? "Yes" : "No" }}
          </td>
        <td>PXS?: {{ pxs ? "Yes" : "No" }}</td>
        <td>SEIU Hardship: {{ seiu ? "Yes" : "No" }} </td>
      </tr>
    </table>
    <hr />

    <h3>Leave Request</h3>
    <table width="800" class="form-inline">
      <tr class="form-group">
        <td class="input-group">
          <div class="input-group-prepend">
            <label for="leaveStart" class="input-group-text">
              Leave Start:
            </label>
          </div>
          <input
            type="date"
            v-model="startLeaveDate"
            id="leaveStart"
            class="form-control"
            data-toggle="tooltip"
            data-placement="bottom"
            data-trigger="manual"
            placeholder="mm/dd/yyyy"
          />
        </td>
        <td class="input-group">
          <div class="input-group-prepend">
            <label for="leaveEnd" class="input-group-text">
              Leave End:
            </label>
          </div>
          <input
            type="date"
            v-model="endLeaveDate"
            id="leaveEnd"
            class="form-control"
            data-toggle="tooltip"
            data-placement="bottom"
            data-trigger="manual"
            placeholder="mm/dd/yyyy"
          />
        </td>
      </tr>
      <tr class="form-group">
        <td class="input-group">
          <div class="input-group-prepend">
            <label for="hrWeek" class="input-group-text">
              HR/Week:
            </label>
          </div>
          <input type="text" id="hrWeek" v-model="hrs" class="form-control" @keyup="change_hours" />
        </td>
      </tr>
      <tr class="form-group">
        <td class="input-group">
          <div class="input-group-prepend">
            <label class="input-group-text" for="R-select">Reason:</label>
          </div>
          <select id="R-select" class="form-control">
            <option selected disabled hidden>--Option--</option>
            <option value="FMLA/OFLA Continuous Concurrent Leave">FMLA/OFLA Continuous Concurrent Leave</option>
            <option value="FMLA/OFLA Intermittent Concurrent Leave">FMLA/OFLA Intermittent Concurrent Leave</option>
            <option value="ER Administrative Leave (Employee Relations)">ER Administrative Leave (Employee Relations)</option>
            <option value="FMLA Continuous Leave">FMLA Continuous Leave</option>
            <option value="FMLA Intermittent Leave">FMLA Intermittent Leave</option>
            <option value="OFLA Intermittent Leave">FLA Intermittent Leave</option>
            <option value="OFLA Continuous Leave">OFLA Continuous Leave</option>
            <option value="Other Non-FMLA/OFLA Leave">Other Non-FMLA/OFLA Leave</option>
            <option value="PC Pending Certification">Inter</option>
            <option value="Amer. With Disabilities Act (ADA)">Amer. With Disabilities Act (ADA)</option>
            <option value="Injured Worker (workers comp)">Injured Worker (workers comp)</option>
            <option value="AP Paid Administrative Leave (LW1)">P Paid Administrative Leave (LW1)</option>
            <option value="AU Unpaid Administrative Leave (LWOP)">AU Unpaid Administrative Leave (LWOP)</option>
            <option value="Discretionary Leave (intermittent)">Discretionary Leave (intermittent)</option>
            <option value="Discretionary Leave (continuous)">Discretionary Leave (continuous)</option>
          </select>
        </td>
        <td class="input-group">
          <div class="input-group-prepend">
            <label class="input-group-text" for="L-select">
              Leave Status:
            </label>
          </div>
          <select id="L-select" class="form-control">
            <option selected disabled hidden>--Option--</option>
            <option value="FMLA-Female EE's pregnancy and care of newborn">FMLA-Female EE's pregnancy and care of newborn</option>
            <option value="FMLA-Male EE's care of newborn">FMLA-Male EE's care of newborn</option>
            <option value="FMLA-Spouse, child, parent with serious health condition">FMLA-Spouse, child, parent with serious health condition</option>
            <option value="FMLA-EE's own serious health condition">FMLA-EE's own serious health condition</option>
            <option value="FMLA-Newly adopted or newly place foster child">FMLA-Newly adopted or newly place foster child</option>
            <option value="FMLA-Qualifying exigency for family member in military">FMLA-Qualifying exigency for family member in military</option>
            <option value="FMLA-Wounded or ill family member in military-up to 26 wks">FMLA-Wounded or ill family member in military-up to 26 wks</option>
            <option value="Military Leave">Military Leave</option>
            <option value="OFLA-Female EE disabled by pregnancy">OFLA-Female EE disabled by pregnancy</option>
            <option value="OFLA-Female EE's pregnancy and care of newborn">OFLA-Female EE's pregnancy and care of newborn</option>
            <option value="OFLA-Spouse, child, parent with serious health condition">OFLA-Spouse, child, parent with serious health condition</option>
            <option value="OFLA-Male EE's care of newborn">OFLA-Male EE's care of newborn</option>
            <option value="OFLA-EE's own serious health condition">OFLA-EE's own serious health condition</option>
            <option value="OFLA-Newly adopted or newly place foster child">OFLA-Newly adopted or newly place foster child</option>
            <option value="OFLA-Care for EE child sick/injured not serious hom care">OFLA-Care for EE child sick/injured not serious hom care</option>
            <option value="OFLA-Parent-in-law, grndchild, grndparent serious hlth cond">OFLA-Parent-in-law, grndchild, grndparent serious hlth cond</option>
            <option value="OFLA-Bereavement Leave">OFLA-Bereavement Leave</option>
            <option value="OFLA-Same-sex domestic partner serious health condition">OFLA-Same-sex domestic partner serious health condition</option>
            <option value="OFLA-Parent/child of sm-sx domestic ptnr serious hlth cond">OFLA-Parent/child of sm-sx domestic ptnr serious hlth cond</option>
            <option value="ADA only">ADA only</option>
            <option value="ADA/FMLA and/or OFLA">ADA/FMLA and/or OFLA</option>
            <option value="Workers compensation only">Workers compensation only</option>
            <option value="Work Comp/FMLA">Work Comp/FMLA</option>
          </select>
        </td>
      </tr>
      <tr class="form-group">
        <td class="input-group">
          <div class="input-group-prepend">
            <label for="fullTime" class="input-group-text">
              Full Time Leave:
            </label>
          </div>
          <input
            class="form-control"
            type="text"
            v-model="full_time"
            @keyup="total_r"
            id="fullTime"
          />
        </td>
        <td class="input-group">
          <div class="input-group-prepend">
            <label for="interTime" class="input-group-text">
              Intermittent Leave:
            </label>
          </div>
          <input
            class="form-control"
            type="text"
            v-model="inter_time"
            @keyup="total_r"
            id="interTime"
          />
        </td>
      </tr>
    </table>
    <hr />

    <h3>Your Balance</h3>
    <div
      v-for='leaveCode in Object.keys(user.paid_leave_balances)'
      :key="leaveCode">
      {{ leaveCode }}: {{ user.paid_leave_balances[leaveCode] }}
    </div>
    <hr />
    <h3>Leave Plan</h3>
    <div v-if="user.paid_leave_balances['ASIC'] > 40">
      <h6>Want to hold 40 hours vacation leave?</h6>
      <label class="inline-radio">
        <input type="radio" value="yes" v-model="picked">
        Yes (Vacation Leave will change to {{ user.paid_leave_balances['AVAC'] - 40 }})
      </label>
      &nbsp;&nbsp;
      <label class="inline-radio">
        <input type="radio" value="no" v-model="picked">
        No
      </label>
      <br />
      <span>Picked: {{ picked }}</span>
    </div>
    <table width="800">
      <tr>
        <th></th>
        <th>Week</th>
        <th>Protected?</th>
        <th>Leave Type</th>
        <th>% Paid</th>
        <th>Leave Used</th>
      </tr>
      <tr
        v-for="(leavePlanElement, index) in leavePlan"
        :key="index"
      >
        <!-- TODO: add logic to below -->
        <td v-if="index==0||leavePlanElement.week!=leavePlan[index-1].week">
          <button @click="addLeaveType(index)" class="btn btn-info">Add Leave Type</button>
        </td>
        <td v-else>
          <button @click="removeLeaveType(index)" class="btn btn-danger">Remove Leave Type</button>
        </td>
        <td>
          &nbsp;{{ leavePlanElement.week }}
        </td>
        <td>&nbsp;{{ protect(index,leavePlan[index].leaveType) }}</td>
        <td>
          <select
            v-model="leavePlanElement.leaveType"
            @keyup="updateSummary"
            class="form-control"
          >
            <option
              v-for="leaveType in leaveTypes"
              :value="leaveType.value"
              :key="leaveType.value"
              :disabled="!validLeaveType(index, leaveType.value)"
            >{{ leaveType.type }}</option>
          </select>
        </td>
        <td>&nbsp;{{ paid_percent(leavePlanElement.leaveType) }}</td>
        <td>
          <input
            type="text"
            v-model="leavePlanElement.leaveUsed"
            @keyup="updateSummary"
            class="form-control"
          />
        </td>
      </tr>
    </table>
    <div class="input-group">
      <div class="input-group-prepend">
        <label for="notes" class="input-group-text">Notes:</label>
      </div>
      <textarea v-model="notes" id="notes" class="form-control"></textarea>
    </div>
    <h3>Leave Summary</h3>
    <table width="400">
      <tr v-for="(amount, index) in leaveSummary" :key="index">
        <td>{{ leaveTypes[index].type }}</td>
        <td>{{ amount }}</td>
      </tr>
      <tr>
        <td><h4>Total</h4></td>
        <td>{{ total }}</td>
      </tr>
    </table>
    <hr />
  </div>
  <div v-else-if="!isAdmin">
    <router-link to="/" class="nav-item nav-link" tag="li" active-class="active"><a>Login</a></router-link>
  </div>
</template>

<script>
import moment from 'moment'
import $ from 'jquery'
import 'bootstrap'
export default {
  name: 'report',
  props: ['user', 'isAdmin', 'Nodes'],
  data: () => ({
    errors: {
      leaveStart: {
        empty:   "Input the date you'd like to start your leave",
        invalid: "Input a start date that occurs before the given end date",
        past:    "Input a start date after today"
      },
      leaveEnd:  {
        empty:   "Input the date you'd like to end your leave",
        invalid: "Input an end date that occurs after the given start date",
      }
    },
    notes: '',
    total_request: 0.0,
    full_time: 0.0,
    inter_time: 0.0,
    hrs: 0.0,
    numWeeks: 0,
    startLeaveDate: '10/10/2019',
    endLeaveDate: '12/12/2019',
    picked: '',
    numWeeks: 0,
    leavePlan: [],

    leaveTypes: [
      { type: 'Sick',         value: 'LTS' },
      { type: 'Vacation',     value: 'LTV' },
      { type: 'AAUP/SEIU',    value: 'LW1' },
      { type: 'STD',          value: 'STD' },
      { type: 'Unpaid Leave', value: 'LW3' },
      { type: 'FLSA/NLFA',    value: 'LSA' },
      { type: 'Personal Day', value: 'Per' },
    ],
    leaveSummary: [
      0.0, // LTS
      0.0, // LTV
      0.0, // LW1
      0.0, // STD
      0.0, // LW3
      0.0, // LSA
      0.0, // Per
    ],
  }),
  computed: {
    std_hours: function() {
      let weeks = 0
      for(let i = 0; i < this.user.stack.length; i++) {
        let edge = this.Nodes[this.user.stack[i].node].options[this.user.stack[i].edge]
        if(edge.type === 'STD')
          weeks += edge.weeks
      }
      return 40 * this.user.fte * weeks
    },
    unpaid_hours: function(){
      let NoUnpaid_total = 0.0
      for(var week in this.leavePlan) {
        if(this.leavePlan[week].leaveType !== 'LW3')
            NoUnpaid_total += parseFloat(this.leavePlan[week].leaveUsed)
          }
      return (this.user.max_protected_leave_hrs - this.user.protected_leave_hrs_taken) - NoUnpaid_total
    },
    dslb: function(){
      return this.aaup ? this.user.fte*320 : 0
    },
    lst: function () {
      return this.user.deductions_eligibility.includes("LST")
    },
    pxs: function () {
      return this.user.deductions_eligibility.includes("PXS")
    },
    aaup: function () {
      return this.user.deductions_eligibility.includes("AAUP")
    },
    seiu: function () {
      return this.user.deductions_eligibility.includes("SEIU")
    },
    total: function() {
      let total = 0.0
      for(var type in this.leaveSummary) {
        total += parseFloat(this.leaveSummary[type])
      }
      return total
    }
  },
  mounted: function() {
    $('#leaveStart').attr('title', this.errors.leaveStart.empty)
    $('#leaveEnd').attr('title', this.errors.leaveEnd.empty)
    $('#leaveStart, #leaveEnd').addClass("error").tooltip('show')
  },
  watch: {
    startLeaveDate: function() {
      this.checkValidDates()
    },
    endLeaveDate: function() {
      this.checkValidDates()
    },
  },
  beforeRouteLeave(to, from, next) {
    $('[data-toggle = "tooltip"]').tooltip('dispose')
    next()
  },
  methods: {
    updateSummary () {
      this.leaveSummary = [
        0.0, // LTS
        0.0, // LTV
        0.0, // LW1
        0.0, // STD
        0.0, // LW3
        0.0, // LSA
        0.0, // Per
      ]
      for(var week in this.leavePlan) {
        for(var type in this.leaveSummary) {
          if(this.leavePlan[week].leaveType === this.leaveTypes[type].value && this.leavePlan[week].leaveUsed !== '') {
            this.leaveSummary[type] += parseFloat(this.leavePlan[week].leaveUsed)
          }
        }
      }
    },
    addLeaveType(index) {
      this.leavePlan.splice(index, 0, Object.assign({}, this.leavePlan[index]))
    },
    removeLeaveType(index) {
      this.leavePlan.splice(index, 1)
    },
    change_hours() {
      for(var index in this.leavePlan) {
        this.leavePlan[index].leaveUsed = parseFloat(this.hrs)
      }
    },
    total_r() {
      this.total_request = 0.0
      this.total_request = parseFloat(this.full_time) + parseFloat(this.inter_time)
    },
    validLeaveType(leavePlanIndex, leaveType) {
      let currentLeaveBalances = Object.assign({}, this.user.paid_leave_balances)
      let leavePlanElement = this.leavePlan[leavePlanIndex]
      for(var index in this.leavePlan) {
        if(index !== leavePlanIndex) {
          switch(this.leavePlan[index].leaveType) {
            case 'LTS':
              currentLeaveBalances['ASIC'] -= this.leavePlan[index].leaveUsed
              break;
          }
        }
      }

      if(this.lst) {
        if(leavePlanElement.week == 1 && currentLeaveBalances['ASIC'] > 0) {
          return leaveType === 'LTS'
        } else if(leavePlanElement.week <= 7
                  || (leavePlanElement.week === 1 && currentLeaveBalances['ASIC'] === 0)) {
          return leaveType === 'STD' || currentLeaveBalances['ASIC'] > 0
        } else {
          return true
        }
      } else {
        if(currentLeaveBalances['ASIC'] > 0) {
          return leaveType === 'LTS'
        } else {
          return true
        }
      }
    },
    setNumWeeks() {
      var duration = moment.duration(moment(this.endLeaveDate).diff(moment(this.startLeaveDate)));
      var numWeeks = duration.asWeeks();

      // Add missing weeks
      for(let weekIndex = this.numWeeks; weekIndex < numWeeks; weekIndex++) {
        this.leavePlan.push({ week: weekIndex + 1, leaveType: '', leaveUsed: 0.0 })
      }
      // Remove extra weeks
      for(let weekIndex = numWeeks; weekIndex < this.numWeeks; weekIndex++) {
        // TODO: handle multiple leavetypes for removed weeks
        this.leavePlan.pop()
      }
      this.numWeeks = numWeeks
    },

    paid_percent(type) {
      if(type!="STD")
        return 100
        else {
          return 60
        }
    },
    protect(week,type){
      let protect_total = 0.0
      for(let weekIndex = 0; weekIndex <= week; weekIndex++) {
        if(type !== '') {
          if(this.leavePlan[weekIndex].leaveType===type) {
            protect_total+= parseFloat(this.leavePlan[weekIndex].leaveUsed)
            console.log(type)
            console.log(protect_total)
          }
        }
      }
      if(type === 'LTS' && (protect_total > this.user.paid_leave_balances['ASIC'] || !this.user.paid_leave_balances['ASIC'])) {
        return 'No'
      } else if (type === 'LTV' && (protect_total > this.user.paid_leave_balances['AVAC'] || !this.user.paid_leave_balances['AVAC'])) {
        return 'No'
      } else if (type === 'Per' && (protect_total > this.user.paid_leave_balances['PERS'] || !this.user.paid_leave_balances['PERS'])) {
        return 'No'
      } else if (type === 'LSA' && (protect_total > this.user.paid_leave_balances['FLSA'] || !this.user.paid_leave_balances['FLSA'])) {
        return 'No'
      } else if (type === 'LW1' && protect_total > this.dslb) {
        return 'No'
      } else if (type === 'LW3' && protect_total > this.unpaid_hours) {
        return 'No'
      } else {
        return 'Yes'
      }
    },
    // When the start and end dates are changed, this function will be called.
    // If the dates are invalid, a tooltip will appear informing the user.
    checkValidDates() {
      let startDate = moment(this.startLeaveDate)
      let endDate = moment(this.endDate)
      let today = moment()
      if(!this.startLeaveDate) {
        $('#leaveStart')
          .addClass('error')
          .tooltip('dispose')
          .attr('title', this.errors.leaveStart.empty)
          .tooltip('show')
      } else if(startDate <= today) {
        $('#leaveStart')
          .addClass('error')
          .tooltip('dispose')
          .attr('title', this.errors.leaveStart.past)
          .tooltip('show')
      } else if(this.endLeaveDate && startDate >= endDate) {
        $('#leaveEnd')
          .addClass('error')
          .tooltip('dispose')
          .attr('title', this.errors.leaveStart.past)
          .tooltip('show')
      } else if(!this.endLeaveDate) {
        $('#leaveStart')
          .removeClass('error')
          .tooltip('dispose')
          .attr('title', '')
      }

      if(!this.endLeaveDate) {
        $('#leaveEnd')
          .addClass('error')
          .tooltip('dispose')
          .attr('title', this.errors.leaveEnd.empty)
          .tooltip('show')
      } else if(!this.startLeaveDate) {
        $('#leaveEnd')
          .removeClass('error')
          .tooltip('dispose')
          .attr('title', '')
      } else if (startDate > today) {
        if(startDate < endDate) {
          $('#leaveStart, #leaveEnd')
            .removeClass('error')
            .tooltip('dispose')
            .attr('title', '')
          this.setNumWeeks()
        } else {
          $('#leaveStart').attr('title', this.errors.leaveStart.invalid)
          $('#leaveEnd').attr('title', this.errors.leaveEnd.invalid)
          $('#leaveStart, #leaveEnd').tooltip('dispose').addClass('error').tooltip('show')
        }
      }
    },
  }
}
</script>
<style>
  .error {
    border: 1px solid red;
  }
</style>
