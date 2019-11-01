<template>
  <div id="report">
    <h1>Portland State University Leave Worksheet</h1>
    <hr>
    <hr>
    <h3>Employee Information</h3>
    <table>
      <tr>
        <td>Employee Name: {{1}}</td>
        <td>Date: {{2}}</td>
      </tr>
      <tr>
        <td>Hire Date: {{1}}</td>
        <td>PSU ID#:{{2}}</td>
      </tr>
      <tr>
        <td>Job Title: {{1}}</td>
        <td>Supervisor: {{2}}</td>
      </tr>
      <tr>
        <td>Payrate {{1}}</td>
      </tr>
    </table>
    <hr>
    <h3>Eligibility</h3>
    <table>
      <tr>
        <td>Look Back Hours: {{1}}</td>
        <td>FTE: {{2}}</td>
      </tr>
      <tr>
        <td>Months : {{1}}</td>
        <td>E-Class: {{2}}</td>
      </tr>
      <tr>
        <td>FMLA: {{1}}</td>
        <td>OFLA: {{2}}</td>
      </tr>
      <tr>
        <td>Hours Eligible: {{1}}</td>
        <td>* {{2}}</td>
      </tr>
      <tr>
        <td>Worksite Location: {{1}}</td>
        <td>Due to a Work Related Injury? {{2}}</td>
      </tr>
    </table>

    <hr>
    <h3>Leave Balance</h3>
    <table>
      <tr>
        <td><b>Total Paid Leave Available: {{1}}</b></td>
        <td><b>Total Leave Request: {{2}} </b></td>
      </tr>
      <tr>
        <td>Sick Leave: {{1}}</td>
        <td>FSLA</td>
        <td>Personal: {{2}}</td>
        <td>AAUP DSLB: {{3}}</td>
      </tr>
      <tr>
        <td>Vacation Leave: {{1}}</td>
        <td>NSLA</td>
        <td>Exchange: {{2}}</td>
        <td>DSLB Total: {{3}}</td>
      </tr>
      <tr>
        <td>ST Disability?: {{1}}</td>
        <td>PXS?:{{2}}</td>
        <td>SEIU Hardship: {{2}}</td>
      </tr>
    </table>
    <hr>
    <h3>Leave Request</h3>
    <table>
      <tr>
        <td>Leave Start: {{1}}</td>
        <td>Intermittent Start: {{2}}</td>
        <td>HR/Week: {{3}}</td>
      </tr>
      <tr>
        <td>Leave End: {{1}}</td>
        <td>Intermittent End: {{2}}</td>
      </tr>
      <tr>
        <td>Reason: {{1}}</td>
        <td>Leave Status: {{2}}</td>
      </tr>
      <tr>
        <td>Full Time Leave {{1}}</td>
        <td>Intermittent Leave {{2}}</td>
      </tr>
    </table>
    <hr>
    <h3>Leave Plan</h3>
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
      <tr v-for="(week, index) in leavePlan">
        <td>{{index + 1}}</td>
        <td><input/></td>
        <td><input type="text" v-model="week.leaveType" v-on:keyup="updateSummary"/></td>
        <td><input/></td>
        <td><input type="number" v-model="week.leaveUsed" v-on:keyup="updateSummary"/></td>
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
    <button v-on:click="addWeek">Add week</button>
    <p><b>Notes:</b><textarea v-model="notes"></textarea></p>
    <h3>Leave Summary</h3>
    <table>
      <tr v-for="type in leaveSummary">
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
    <button v-on:click="GeneratePdf">Generate PDF</button>
  </div>
</template>

<script>
export default {
    name: 'report',
    data: () => ({
        notes: '',
        total: 0,
        leavePlan: [
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
            {leaveType: '', leaveUsed: 0},
        ],
        leaveSummary: [
            {real: 'Sick', name: 'LTS', hours: 0},
            {real: 'Vacation', name: 'LTV', hours: 0},
            {real: 'AAUP/SEIU', name: 'LW1', hours: 0},
            {real: 'STD', name: 'STD', hours: 0},
            {real: 'Unpaid Leave', name: 'LW3', hours: 0},
            {real: 'FLSA/NLFA', name: 'LSA', hours: 0},
            {real: 'Personal Day', name: 'Per', hours: 0},
        ],
    }),
    methods: {
        updateSummary() {
            this.leaveSummary = [
                {real: 'Sick', name: 'LTS', hours: 0},
                {real: 'Vacation', name: 'LTV', hours: 0},
                {real: 'AAUP/SEIU', name: 'LW1', hours: 0},
                {real: 'STD', name: 'STD', hours: 0},
                {real: 'Unpaid Leave', name: 'LW3', hours: 0},
                {real: 'FLSA/NLFA', name: 'LSA', hours: 0},
                {real: 'Personal Day', name: 'Per', hours: 0},
            ]
            for (week in this.leavePlan) {
                for (type in this.leaveSummary) {
                    if (this.leavePlan[week].leaveType == this.leaveSummary[type].name)
                        this.leaveSummary[type].hours += parseInt(this.leavePlan[week].leaveUsed)
                }
            }
            this.total = 0
            for (week in this.leavePlan) {
                for (type in this.leaveSummary) {
                    if (this.leavePlan[week].leaveType == this.leaveSummary[type].name)
                        if (this.leavePlan[week].leaveUsed != 0) {
                            this.total += parseInt(this.leavePlan[week].leaveUsed)
                        }
                }
            }
        },
        addWeek() {
            this.leavePlan.push({leaveType: '', leaveUsed: 0})
        }
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
}
</style>
