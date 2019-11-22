<template>
  <div id="report">
    <h1>Portland State University Leave Worksheet</h1>
    <hr />
    <hr />
    <h3>Employee Information</h3>
    <table>
      <tr>
        <td>Employee Name: {{user.first_name}} {{user.last_name}}</td>
        <td>Date: {{new Date().toDateString()}}</td>
      </tr>
      <tr>
        <td>Hire Date: {{user.hire_date}}</td>
        <td>PSU ID#:{{user.employee_id}}</td>
      </tr>
      <!--
        <tr>
          <td>Job Title: {{0}}  </td>
          <td>Supervisor: {{0}} </td>
        </tr>
      -->
      <tr>
        <td>Payrate {{0}}</td>
      </tr>
    </table>
    <hr />
    <h3>Eligibility</h3>
    <table>
      <tr>
        <td>Look Back Hours: {{user.month_lookback_12}}</td>
        <td>FTE: {{user.fte}}</td>
      </tr>
      <tr>
        <td>Months : {{0}}</td>
        <td>E-Class: {{0}}</td>
      </tr>
      <tr>
        <td>FMLA: {{user.fmla_eligibility}}</td>
        <td>OFLA: {{user.ofla_eligibility}}</td>
      </tr>
      <tr>
        <td>Hours Eligible: {{0}}</td>
        <td>* {{0}}</td>
      </tr>
      <tr>
        <td>Worksite Location: {{0}}</td>
        <td>Due to a Work Related Injury? {{0}}</td>
      </tr>
    </table>

    <hr />
    <h3>Leave Balance</h3>
    <table>
      <tr>
        <td>
          <b>Total Paid Leave Available: {{0}}</b>
        </td>
        <td>
          <b>Total Leave Request: {{0}}</b>
        </td>
      </tr>
      <tr>
        <td>Sick Leave: {{0}}</td>
        <td>FSLA</td>
        <td>Personal: {{0}}</td>
        <td>AAUP DSLB: {{0}}</td>
      </tr>
      <tr>
        <td>Vacation Leave: {{0}}</td>
        <td>NSLA</td>
        <td>Exchange: {{0}}</td>
        <td>DSLB Total: {{0}}</td>
      </tr>
      <tr>
        <td>ST Disability?: {{ lst }}</td>
        <td>PXS?: {{ pxs }}</td>
        <td>SEIU Hardship: {{0}}</td>
      </tr>
    </table>
    <hr />
    <h3>Leave Request</h3>
    <table>
      <tr>
        <td>
          Leave Start:
          <input />
        </td>
        <td>
          Intermittent Start:
          <input />
        </td>
        <td>
          HR/Week:
          <input />
        </td>
      </tr>
      <tr>
        <td>
          Leave End:
          <input />
        </td>
        <td>
          Intermittent End:
          <input />
        </td>
      </tr>
      <tr>
        <td>
          Reason:
          <select id="R-select">
            <option value>--Option--</option>
            <option
              value="FMLA/OFLA Continuous Concurrent Leave"
            >FMLA/OFLA Continuous Concurrent Leave</option>
            <option value="Inter">Inter</option>
          </select>
        </td>
        <td>
          Leave Status:
          <select id="L-select">
            <option value>--Option--</option>
            <option
              value="FMLA-Female EE's pregnancy and care of newborn"
            >FMLA-Female EE's pregnancy and care of newborn</option>
            <option value="Inter">Inter</option>
          </select>
        </td>
      </tr>
      <tr>
        <td>
          Full Time Leave
          <input />
        </td>
        <td>
          Intermittent Leave
          <input />
        </td>
      </tr>
    </table>
    <hr />
    <h3>Leave Balance</h3>
    <div v-for="(u, index) in user.paid_leave_balances" :key="index">
      <div v-if=" u[1] !== 0">{{u[0]}}: {{u[1]}}</div>
    </div>
    <hr />
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
      <tr v-for="(week, index) in leavePlan" :key="index">
        <td>{{index + 1}}</td>
        <td>
          <input />
        </td>
        <td>
          <input type="text" v-model="week.leaveType" v-on:keyup="updateSummary" />
        </td>
        <td>
          <input />
        </td>
        <td>
          <input type="text" v-model="week.leaveUsed" v-on:keyup="updateSummary" />
        </td>
        <td>
          <select id="CI-select">
            <option value>--Option--</option>
            <option value="Cont">Cont</option>
            <option value="Inter">Inter</option>
          </select>
        </td>
        <td>
          <input />
        </td>
        <td>
          <input />
        </td>
      </tr>
    </table>
    <div id="addWeek">
      <button v-on:click="addWeek">Add week</button>
    </div>
    <p>
      <b>Notes:</b>
      <textarea v-model="notes"></textarea>
    </p>
    <h3>Leave Summary</h3>
    <table>
      <tr v-for="(type, index) in leaveSummary" :key="index">
        <td>{{type.real}}</td>
        <td>{{type.name}}</td>
        <td>{{type.hours}}</td>
      </tr>
      <tr>
        <td>
          <h4>Total</h4>
        </td>
        <td>{{total}}</td>
      </tr>
      <tr>
        <button class="btn btn-success" @click="saveAsNewReport">Save As New Report</button>
        <button class="btn btn-success" @click="saveReport">Update Report</button>
      </tr>
    </table>
    <hr />
  </div>
</template>

<script>
export default {
  name: "report",
  props: ["user", "auth", "report", "report-id"],
  data: () => ({
    saveError: "",
    notes: "",
    Lts: "Yes",
    total: 0.0,
    leavePlan: [
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 },
      { leaveType: "", leaveUsed: 0.0 }
    ],
    leaveSummary: [
      { real: "Sick", name: "LTS", hours: 0.0 },
      { real: "Vacation", name: "LTV", hours: 0.0 },
      { real: "AAUP/SEIU", name: "LW1", hours: 0.0 },
      { real: "STD", name: "STD", hours: 0.0 },
      { real: "Unpaid Leave", name: "LW3", hours: 0.0 },
      { real: "FLSA/NLFA", name: "LSA", hours: 0.0 },
      { real: "Personal Day", name: "Per", hours: 0.0 }
    ]
  }),
  computed: {
    lst: function() {
      return this.user.deductions_eligibility.includes("LST") ? "Yes" : "No";
    },
    pxs: function() {
      return this.user.deductions_eligibility.includes("PXS") ? "Yes" : "No";
    }
  },

  methods: {
    updateSummary() {
      this.leaveSummary = [
        { real: "Sick", name: "LTS", hours: 0.0 },
        { real: "Vacation", name: "LTV", hours: 0.0 },
        { real: "AAUP/SEIU", name: "LW1", hours: 0.0 },
        { real: "STD", name: "STD", hours: 0.0 },
        { real: "Unpaid Leave", name: "LW3", hours: 0.0 },
        { real: "FLSA/NLFA", name: "LSA", hours: 0.0 },
        { real: "Personal Day", name: "Per", hours: 0.0 }
      ];
      for (var week in this.leavePlan) {
        for (var type in this.leaveSummary) {
          if (this.leavePlan[week].leaveType == this.leaveSummary[type].name)
            this.leaveSummary[type].hours += parseFloat(
              this.leavePlan[week].leaveUsed
            );
        }
      }
      this.total = 0.0;
      for (var week in this.leavePlan) {
        for (var type in this.leaveSummary) {
          if (this.leavePlan[week].leaveType == this.leaveSummary[type].name)
            if (this.leavePlan[week].leaveUsed != 0) {
              this.total += parseFloat(this.leavePlan[week].leaveUsed);
            }
        }
      }
    },
    addWeek() {
      this.leavePlan.push({ leaveType: "", leaveUsed: 0.0 });
    },
    saveAsNewReport() {
      //This function will allow admin/user to save a copy of the report
      //they are working on, preserving the current report
      var data = JSON.stringify({
        EMPLOYEE_ID: this.user.employee_id,
        REPORT: this.leavePlan
      });

      fetch("http://localhost:8000/database/savereport/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: this.auth
        },
        body: data
      })
        .then(response => {
          if (response.ok) {
            throw Error("Saving report failed.");
          }
          return response.json();
        })
        .then(data => {
          console.log(JSON.stringify(data));
        })
        .catch(error => {
          this.saveError = error;
        });
      this.$emit("update-employee");
    },
    saveReport() {
      //This function will allow admin/user to save the new updates of
      //the report they are working on to itself
      var tosend = JSON.stringify({
        REPORT_ID: this.reportId,
        EMPLOYEE_ID: this.user.employee_id,
        REPORT: this.leavePlan
      });
      fetch("http://localhost:8000/database/updatereport/", {
        method: "POST",
        body: tosend,
        headers: {
          "Content-Type": "application/json",
          Authorization: this.auth
        }
      });
      this.$emit("update-employee");
    }
  }
};
</script>
<!-- styling for the component -->
<style>
#report {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
