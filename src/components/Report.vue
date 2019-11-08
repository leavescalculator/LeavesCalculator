<template>
  <div id="report">
      <h1>Portland State University Leave Worksheet</h1>
      <hr><hr>
      <h3>Employee Information</h3>
      <table width="800">
        <tr>
          <td>Employee Name: {{user.first_name}} {{user.last_name}} </td>
          <td>Date: {{new Date().toDateString()}}</td>
        </tr>
        <tr>
          <td>Hire Date: {{user.hire_date}}</td>
          <td>PSU ID#:{{user.employee_id}}</td>
        </tr>
        <tr>
          <td>Payrate {{0}}  </td>
        </tr>
      </table>
      <hr>
    <h3>Eligibility</h3>
      <table width="800">
        <tr>
          <td>Look Back Hours: {{user.month_lookback_12}}  </td>
          <td>FTE: {{user.fte}}</td>
        </tr>
        <tr>
          <td>Months : {{0}}  </td>
          <td>E-Class: {{0}}</td>
        </tr>
        <tr>
          <td>FMLA: {{user.fmla_eligibility}}  </td>
          <td>OFLA: {{user.ofla_eligibility}}</td>
        </tr>
        <tr>
          <td>Hours Eligible: {{0}}  </td>
          <td>* {{0}}</td>
        </tr>
        <tr>
          <td>Worksite Location: {{0}}  </td>
          <td>Due to a Work Related Injury?		 {{0}}</td>
        </tr>
      </table>

      <hr>
    <h3>Leave Balance</h3>
    <table width="800">
      <tr>
        <td><b>Total Paid Leave Available: {{0}}</b></td>
        <td><b>Total Leave Request: {{total_request}} </b></td>
      </tr>
      <tr>
        <td>
          <div v-for='(u, index) in user.paid_leave_balances' :key="index">
            <div v-if=" u.leave_code == 'ASIC' ">
              Sick Leave: {{u.balance}}
            </div>
        </div>
        </td>
        <td>FSLA</td>
        <td><div v-for='(u, index) in user.paid_leave_balances' :key="index">
          <div v-if=" u.leave_code == 'PERS' ">
            Personal Leave: {{u.balance}}
          </div>
        </div>
          </td>
        <td>AAUP DSLB: {{aaup}} </td>
      </tr>
      <tr>
        <td>
          <div v-for='(u, index) in user.paid_leave_balances' :key="index">
            <div v-if=" u.leave_code == 'AVAC' ">
              Vacation Leave: {{u.balance}}
            </div>
          </div> </td>
        <td>NSLA</td>
        <td><div v-for='(u, index) in user.paid_leave_balances' :key="index">
          <div v-if=" u.leave_code == 'XCHG' ">
            Exchange: {{u.balance}}
          </div>
        </div> </td>
        <td><div v-if="aaup==='Yes'">
          DSLB Total: {{user.fte*320}}
        </div>
          <div v-else>
            DSLB Total: {{0}}
        </div>
        </td>
      </tr>
      <tr>
        <td>ST Disability?: {{ lst }}
          </td>
        <td>PXS?: {{ pxs }}</td>
        <td>SEIU Hardship: {{seiu}} </td>
      </tr>
    </table>
    <hr>
    <h3>Leave Request</h3>
    <table width="800">
      <tr>
        <td>Leave Start:<input type="date"/>  </td>
        <td>Intermittent Start: <input type="date"/></td>
        <td>HR/Week: <input /></td>
      </tr>
      <tr>
        <td>Leave End: <input type="date"/> </td>
        <td>Intermittent End: <input type="date"/></td>
      </tr>
      <tr>
        <td>Reason:<select id="R-select">
        <option value="">--Option--</option>
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
        </select></td>
        <td>Leave Status: <select id="L-select">
        <option value="">--Option--</option>
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
        </select> </td>
      </tr>
      <tr>
        <td>Full Time Leave <input type="text" v-model="full_time" v-on:keyup="total_r"/> </td>
        <td>Intermittent Leave <input type="text" v-model="inter_time"v-on:keyup="total_r"/> </td>
      </tr>
    </table>
    <hr>
    <h3>Your Balance</h3>
    <div v-for='(u, index) in user.paid_leave_balances' :key="index">
      <div v-if=" u.balance !== 0">
        {{u.leave_code}}: {{u.balance}}
      </div>
  </div>
    <hr>
    <h3>Leave Plan</h3>
    <div v-for='(u, index) in user.paid_leave_balances' :key="index">
      <div v-if=" u.leave_code == 'ASIC' && u.balance > 40">
        <h6>Want to hold 40 hours sick leave?</h6>
        <input type="radio" id="yes" value="Yes" v-model="picked">
        <label for="yes">Yes (sick leave will change to {{u.balance-40}})</label>
        &nbsp;&nbsp;
        <input type="radio" id="no" value="No" v-model="picked">
        <label for="no">No</label>
        <br>
        <span>Picked: {{ picked }}</span>
      </div>
    </div>
    <table>
      <tr>
        <th>Week</th>
        <th>Protected?</th>
        <th>LeaveType</th>
        <th>% Paid</th>
        <th>LeaveUsed</th>
        <th>Cont/Inter</th>
        <th>%</th>
        <th>Pay</th>
      </tr>
      <tr v-for="weekPlan in leavePlan" :key="index">
        <td><input type="text" v-model="weekPlan.week"/></td>
        <td><input/></td>
        <td><input type="text" v-model="weekPlan.leaveType" v-on:keyup="updateSummary"/></td>
        <td><input/></td>
        <td><input type="text" v-model="weekPlan.leaveUsed" v-on:keyup="updateSummary"/></td>
        <td>
          <select id="CI-select">
            <option value="">--Option--</option>
            <option value="Cont">Cont</option>
            <option value="Inter">Inter</option>
          </select>
        </td>
        <td><input/></td>
        <td><input/></td>
      </tr>
    </table>
    <div id='addWeek'>
  <button v-on:click="addWeek">Add week</button>
</div>
    <p><b>Notes:</b><textarea v-model="notes"></textarea></p>
    <h3>Leave Summary</h3>
    <table width="400">
      <tr v-for="(type, index) in leaveSummary" :key="index">
        <td>{{type.real}}</td>
        <td>{{type.name}}</td>
        <td>{{type.hours}}</td>
      </tr>
      <tr>
        <td><h4>Total</h4></td>
        <td>{{total}}</td>
      </tr>
    </table>
    <hr>
  </div>
</template>

<script>
export default {
    name: 'report',
    props: ['user'],
  data: () => ({
    notes: '',
    Lts: 'Yes',
    total: 0.0,
    total_request: 0.0,
    full_time:0.0,
    inter_time:0.0,
    sick_leave:0.0,
    picked:'',
    leavePlan: [
      {week:1, leaveType: '', leaveUsed: 0.0 },


    ],
    leaveSummary: [
      {real: 'Sick',name: 'LTS', hours: 0.0},
            {real: 'Vacation', name: 'LTV', hours: 0.0},
            {real: 'AAUP/SEIU', name: 'LW1', hours: 0.0},
            {real: 'STD', name: 'STD', hours: 0.0},
            {real: 'Unpaid Leave', name: 'LW3', hours: 0.0},
            {real: 'FLSA/NLFA', name: 'LSA', hours: 0.0},
            {real: 'Personal Day', name: 'Per', hours: 0.0},
    ],
  }),
  computed:{
    lst: function () {
      return this.user.deductions_eligibility.includes("LST") ? "Yes" : "No";
    },
    pxs: function () {
      return this.user.deductions_eligibility.includes("PXS") ? "Yes" : "No";
    },
    aaup: function () {
      return this.user.deductions_eligibility.includes("AAUP") ? "Yes" : "No";
    },
    seiu: function () {
      return this.user.deductions_eligibility.includes("SEIU") ? "Yes" : "No";
    },
  },

  methods: {
    updateSummary () {
      this.leaveSummary = [
        { real: 'Sick',         name: 'LTS', hours: 0.0 },
        { real: 'Vacation',     name: 'LTV', hours: 0.0 },
        { real: 'AAUP/SEIU',    name: 'LW1', hours: 0.0 },
        { real: 'STD',          name: 'STD', hours: 0.0},
                {real: 'Unpaid Leave', name: 'LW3', hours: 0.0 },
        { real: 'FLSA/NLFA',    name: 'LSA', hours: 0.0 },
        { real: 'Personal Day', name: 'Per', hours: 0.0 },
      ]
      for(var week in this.leavePlan){
        for(var type in this.leaveSummary){
          if(this.leavePlan[week].leaveType==this.leaveSummary[type].name)
            this.leaveSummary[type].hours += parseFloat(this.leavePlan[week].leaveUsed)
                }
            }
            this.total = 0.0
            for (var week in this.leavePlan){
        for(var type in this.leaveSummary){
          if(this.leavePlan[week].leaveType==this.leaveSummary[type].name)
            if(this.leavePlan[week].leaveUsed != 0){this.total += parseFloat(this.leavePlan[week].leaveUsed)
                        }
                }
            }
        },
        addWeek() {
            this.leavePlan.push({leaveType: '', leaveUsed: 0.0 })
    },
        total_r(){
          this.total_request = 0.0
          this.total_request = parseFloat(this.full_time) + parseFloat(this.inter_time)
        },

    }
}
</script>
<!-- styling for the component -->
<style>
#report {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  width: 800px
}
</style>
