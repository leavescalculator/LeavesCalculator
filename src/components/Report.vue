<template>
  <div id="report">
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
        <td><div v-if="aaup">
          DSLB Total: {{ user.fte*320 }}
        </div>
          <div v-else>
            DSLB Total: {{ 0 }}
        </div>
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
        <td class="col input-group">
          <div class="input-group-prepend">
            <label for="leaveStart" class="input-group-text">
              Leave Start:
            </label>
          </div>
          <input type="date" v-model="startLeaveDate" id="leaveStart" class="form-control" v-on:keyup="change_hours()"/>
        </td>
        <td class="col input-group">
          <div class="input-group-prepend">
            <label for="hrWeek" class="input-group-text" >
              HR/Week:
            </label>
          </div>
          <input type="text" id="hrWeek" v-model="hrs" class="form-control" v-on:keyup="change_hours()"/>
        </td>
      </tr>
      <tr class="form-group">
        <td class="col input-group">
          <div class="input-group-prepend">
            <label for="leaveEnd" class="input-group-text">
              Leave End:
            </label>
          </div>
          <input type="date" v-model="endLeaveDate" id="leaveEnd" class="form-control" v-on:keyup="change_hours()"/>
        </td>
      </tr>
      <tr class="form-group">
        <td class="col input-group">
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
        <td class="col input-group">
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
        <td class="col input-group">
          <div class="input-group-prepend">
            <label for="fullTime" class="input-group-text">
              Full Time Leave:
            </label>
          </div>
          <input
            class="form-control"
            type="text"
            v-model="full_time"
            v-on:keyup="total_r"
            id="fullTime"
          />
        </td>
        <td class="col input-group">
          <div class="input-group-prepend">
            <label for="interTime" class="input-group-text">
              Intermittent Leave:
            </label>
          </div>
          <input
            class="form-control"
            type="text"
            v-model="inter_time"
            v-on:keyup="total_r"
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
        <th>Week</th>
        <th>Protected?</th>
        <th>LeaveType</th>
        <th>% Paid</th>
        <th>LeaveUsed</th>
        <th>%</th>
        <th>Pay</th>
      </tr>
      <tr v-for="(leavePlanElement, index) in leavePlan">
        <td>
          &nbsp; {{leavePlanElement.week}}
        </td>
        <td>{{leavePlanElement.protected}}</td>
        <td>
          <select
            v-model="leavePlanElement.leaveType"
            v-on:keyup="updateSummary"
            class="form-control"
          >
            <option
              v-for="leaveType in leaveTypes"
              :value="leaveType.value"
              :key="leaveType.value"
              :disabled="!validLeaveType(index, leaveType.value)"
            >{{ leaveType.type }}</option>
          </select>
          <div id="tooltipBox"></div>
        </td>
        <td>&nbsp;{{leavePlanElement.paid}}</td>
        <td>
          <input
            type="text"
            v-model="leavePlanElement.leaveUsed"
            v-on:keyup="updateSummary"
            class="form-control"
          />
        </td>
        <td>&nbsp;{{leavePlanElement.percent}}</td>
        <td>&nbsp;{{leavePlanElement.pay}}</td>
        <div id='addWeek'>
          <button v-on:click="addWeek(index)" v-model="index" class="btn btn-info">Add LeaveType</button>
        </div>
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
      <tr v-for="(type, index) in leaveSummary" :key="index">
        <td>{{ leaveTypes[index].type }}</td>
        <td>{{ leaveTypes[index].value }}</td>
        <td>{{ type }}</td>
      </tr>
      <tr>
        <td><h4>Total</h4></td>
        <td>{{ total }}</td>
      </tr>
    </table>
    <hr />
  </div>
</template>

<script>
export default {
  name: 'report',
  props: ['user'],
  data: () => ({
    notes: '',
    Lts: 'Yes',
    total_request: 0.0,
    full_time: 0.0,
    inter_time: 0.0,
    sick_leave: 0.0,
    hrs: 0.0,
    index:0,
    startInterDate:"",
    startLeaveDate:"",
    endInterDate:"",
    endLeaveDate:"",
    picked:'',
    leavePlan: [
      { week:1, protected:'', leaveType: '',paid:0.0, leaveUsed: 0.0, percent:0.0, pay:0.0 },
      { week:2, protected:'', leaveType: '',paid:0.0, leaveUsed: 0.0, percent:0.0, pay:0.0 },
      { week:3, protected:'', leaveType: '',paid:0.0, leaveUsed: 0.0, percent:0.0, pay:0.0 },
      { week:4, protected:'', leaveType: '',paid:0.0, leaveUsed: 0.0, percent:0.0, pay:0.0 },
      { week:5, protected:'', leaveType: '',paid:0.0, leaveUsed: 0.0, percent:0.0, pay:0.0 },
      { week:6, protected:'', leaveType: '',paid:0.0, leaveUsed: 0.0, percent:0.0, pay:0.0 },
      { week:7, protected:'', leaveType: '',paid:0.0, leaveUsed: 0.0, percent:0.0, pay:0.0 },
      { week:8, protected:'', leaveType: '',paid:0.0, leaveUsed: 0.0, percent:0.0, pay:0.0 },
      { week:9, protected:'', leaveType: '',paid:0.0, leaveUsed: 0.0, percent:0.0, pay:0.0 },
    ],
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
    addWeek(index) {
      this.leavePlan.splice(index,0,{week: this.leavePlan[index].week, protected: '', leaveType: '', paid:0.0, leaveUsed: this.leavePlan[index].leaveUsed, percent:0.0, pay:0.0 })
    },
    change_hours() {
      var shado = require("shado");
      var firstDate = this.startLeaveDate;
      var secondDate = this.endLeaveDate;
      var result = shado.date.setDates(firstDate, secondDate).getWeeks(false)+1;
      console.log(result)

      for(var week in this.leavePlan){
        if(week < result)
        {
          this.leavePlan[week].leaveUsed = parseFloat(this.hrs)
        }
        else {
          this.leavePlan[week].leaveUsed = 0.0
        }
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
    }
  }
}
</script>
<style>
</style>
