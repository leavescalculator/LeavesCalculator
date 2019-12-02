<template>
  <div id="report" v-if="user.employee_id != null">
    <h1>Portland State University Leave Worksheet</h1>
    <hr />

    <h3>Employee Information</h3>
    <table width="800">
      <tr>
        <td>Employee Name: {{ user.first_name }} {{ user.last_name }}</td>
      </tr>
      <tr>
        <td>Hire Date: {{ user.hire_date }}</td>
        <td>PSU ID #: {{ user.psu_id }}</td>
      </tr>
      <tr>
        <td class="input-group">
          <div class="input-group-prepend">
            <label for="payrate" class="input-group-text">Payrate</label>
          </div>
          <input
            type="text"
            v-model="payrate"
            id="payrate"
            class="form-control"
            data-toggle="tooltip"
            data-placement="bottom"
            data-trigger="manual"
          />
        </td>
      </tr>
    </table>
    <hr />

    <h3>Eligibility Status</h3>
    <table width="800">
      <tr>
        <td>Look Back Hours (12 months): {{ user.month_lookback_12 }}</td>
        <td>FTE: {{ user.fte }}</td>
        <td>FMLA: {{ fmlaEligibility }}</td>
      </tr>
      <tr>
        <td>Look Back Hours (6 months): {{ user.month_lookback_6 }}</td>
        <td>E-Class: {{ this.user.employee_classification }}</td>
        <td>OFLA: {{ oflaEligibility }}</td>
      </tr>
      <tr>
        <td
          v-if="fmlaEligibility!=='Not Eligible' && oflaEligibility!=='Not Eligible'"
        >Coverage: FMLA/OFLA</td>
        <td
          v-else-if="fmlaEligibility==='Not Eligible' && oflaEligibility!=='Not Eligible'"
        >Coverage: OFLA</td>
        <td
          v-else-if="fmlaEligibility!=='Not Eligible' && oflaEligibility==='Not Eligible'"
        >Coverage: FMLA</td>
        <!-- TODO: replace above with this when we handle exceptions<td
          v-else-if="fmlaEligibility!=='Not Eligible' && oflaEligibility==='Not Eligible' && !exceptions"
        >Coverage: FMLA</td>-->
        <td v-else>Coverage: ADA</td>
      </tr>
    </table>
    <hr />

    <h3>Reason</h3>
    <div v-for="(path, index) in pathway" :key="index">{{path}}</div>
    <hr />

    <h3>Leave Balance</h3>
    <table width="1200">
      <tr>
        <td>
          <b>Protected Leave Taken: {{ user.protected_leave_hrs_taken }}</b>
        </td>
        <td>
          <b>Total Protected Leave Available: {{ max_protected_leave_hrs }}</b>
        </td>
        <td>
          <b>Total Paid Leave Available: {{ total_paid_leave }}</b>
        </td>
        <td>
          <b>Total Leave Request: {{ total.hours }}</b>
          <!--<b>Total Leave Request: {{ total_request }}</b>-->
        </td>
      </tr>
      <tr>
        <td>ST Disability: {{ lst ? "Yes" : "No" }}</td>
        <td>SEIU Hardship: {{ seiu ? "Yes" : "No" }}</td>
        <td>AAUP DSLB: {{ aaup ? "Yes" : "No" }}</td>
        <td>Flexible Spending for Childcare (PXS): {{ pxs ? "Yes" : "No" }}</td>
      </tr>
      <tr>
        <td>ST Disability Leave: {{this.std_hours}}</td>
        <td>Hardship (Donated) Leave: {{this.hardshipHours}}</td>
        <td>AAUP DSLB Total: {{ dslb }}</td>
        <td>PXS Leave: {{this.pxsHours}}</td>
      </tr>
      <tr>
        <td>Sick Leave: {{ this.sickHours }}</td>
        <td>Vacation Leave: {{ this.vacationHours }}</td>
        <td>Personal Leave: {{ this.personalHours }}</td>
        <td>Bereavement Leave: {{this.bereavementHours}}</td>
      </tr>
      <tr>
        <td>Furlough Leave: {{this.furloughHours}}</td>
        <td>Exchange Leave: {{ this.exchangeHours }}</td>
        <td>NSLA (Comp Time) Leave: {{this.nslaHours}}</td>
        <td>FSLA Leave: {{this.fslaHours}}</td>
      </tr>
      <tr>
        <td>Other Leave: {{this.otherHours}}</td>
      </tr>
    </table>
    <hr />

    <h3>Leave Request</h3>
    <table width="800" class="form-inline">
      <tr class="form-group">
        <td class="input-group">
          <div class="input-group-prepend">
            <label for="leaveStart" class="input-group-text">Leave Start:</label>
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
            <label for="leaveEnd" class="input-group-text">Leave End:</label>
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
            <label for="hrWeek" class="input-group-text">HR/Week:</label>
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
            <option v-for="(reason, index) in reasons" :key="index">{{reason}}</option>
          </select>
        </td>
        <td class="input-group">
          <div class="input-group-prepend">
            <label class="input-group-text" for="L-select">Leave Status:</label>
          </div>
          <select id="L-select" class="form-control">
            <option selected disabled hidden>--Option--</option>
            <option v-for="(leave, index) in leaveStatus" :key="index">{{leave}}</option>
          </select>
        </td>
      </tr>
      <tr class="form-group">
        <td class="input-group">
          <div class="input-group-prepend">
            <label for="fullTime" class="input-group-text">Full Time Leave:</label>
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
            <label for="interTime" class="input-group-text">Intermittent Leave:</label>
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

    <!--<h3>Your Balance</h3>
    <div
      v-for="leaveCode in Object.keys(user.paid_leave_balances)"
      :key="leaveCode"
    >{{ leaveCode }}: {{ user.paid_leave_balances[leaveCode] }}</div>
    <hr />-->
    <h3>Leave Plan</h3>
    <!-- Classified employees can say they want to use hold 40 vacation hours if they have that much-->
    <div v-if="user.paid_leave_balances['AVAC'] >= 40 && this.classifiedEmp">
      <h6>Want to hold 40 hours vacation leave?</h6>
      <label class="inline-radio">
        <input type="radio" value="yes" v-model="classifiedPicked" />
        Yes
      </label>
      &nbsp;&nbsp;
      <label class="inline-radio">
        <input type="radio" value="no" v-model="classifiedPicked" />
        No
      </label>
    </div>
    <!-- Unclassified employees can say they don't want to use vacation hours-->
    <div v-if="user.paid_leave_balances['AVAC'] > 0 && this.unclassifiedEmp">
      <h6>Want to save vacation hours?</h6>
      <label class="inline-radio">
        <input type="radio" value="yes" v-model="unclassifiedPicked" />
        Yes
      </label>
      &nbsp;&nbsp;
      <label class="inline-radio">
        <input type="radio" value="no" v-model="unclassifiedPicked" />
        No
      </label>
    </div>
    <table width="800">
      <tr>
        <th></th>
        <th>Week</th>
        <th>Protected?</th>
        <th>Leave Type</th>
        <th>% Paid</th>
        <th>Leave Used</th>
        <th>Pay</th>
      </tr>
      <tr v-for="(leavePlanElement, index) in leavePlan" :key="index">
        <!-- TODO: add logic to below -->
        <td v-if="index==0||leavePlanElement.week!=leavePlan[index-1].week">
          <button @click="addLeaveType(index)" class="btn btn-info">Add Leave Type</button>
        </td>
        <td v-else>
          <button @click="removeLeaveType(index)" class="btn btn-danger">Remove Leave Type</button>
        </td>
        <td>&nbsp;{{ leavePlanElement.week }}</td>
        <td>&nbsp;{{ protect(index,leavePlan[index].leaveType) }}</td>
        <td>
          <select v-model="leavePlanElement.leaveType" @click="updateSummary" class="form-control">
            <option
              v-for="leaveType in leaveTypes"
              :value="leaveType.value"
              :key="leaveType.value"
              :disabled="!validLeaveType(index, leaveType.value)"
            >{{ leaveType.type }}</option>
          </select>
        </td>
        <td>&nbsp;{{ paid_percent(leavePlanElement.leaveType) }}%</td>
        <td>
          <input
            type="text"
            v-model="leavePlanElement.leaveUsed"
            @keyup="updateSummary"
            class="form-control"
          />
        </td>
        <td>&nbsp;{{ pay(leavePlanElement) }}</td>
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
      <tr>
        <th>Leave Type</th>
        <th>Hours Used</th>
        <th>Pay</th>
      </tr>
      <tr v-for="(amount, index) in leaveSummary" :key="index">
        <td>{{ leaveTypes[index].type }}</td>
        <td>{{ amount }}</td>
        <td v-if="leaveTypes[index].value === 'STD'">${{ (amount * payrate * 0.6).toFixed(2) }}</td>
        <td v-else-if="leaveTypes[index].value === 'LW3'">${{ (amount * payrate * 0).toFixed(2) }}</td>
        <td v-else>${{ (amount * payrate).toFixed(2) }}</td>
      </tr>
      <tr>
        <td>
          <h4>Total</h4>
        </td>
        <td>{{ total.hours }}</td>
        <td>${{ total.pay.toFixed(2) }}</td>
      </tr>
    </table>
    <hr />
  </div>
  <div v-else-if="!isAdmin">
    <router-link to="/" class="nav-item nav-link" tag="li" active-class="active">
      <a>Login</a>
    </router-link>
  </div>
</template>

<script>
import moment from "moment";
import $ from "jquery";
import "bootstrap";
export default {
  name: "report",
  props: ["user", "isAdmin", "Nodes"],
  data: () => ({
    errors: {
      payrate: {
        empty: "Input your hourly income"
      },
      leaveStart: {
        empty: "Input the date you'd like to start your leave",
        invalid: "Input a start date that occurs before the given end date",
        past: "Input a start date after today"
      },
      leaveEnd: {
        empty: "Input the date you'd like to end your leave",
        invalid: "Input an end date that occurs after the given start date"
      },
      leaveHours: {
        invalid: "Input a value that does not exceed your max available hours"
      }
    },
    classifiedEmpList: ["CA", "CB", "CD", "CE", "GI", "GJ"],
    unclassifiedEmpList: [
      "TS",
      "UA",
      "UB",
      "UC",
      "UD",
      "UE",
      "UF",
      "UG",
      "UH",
      "UT",
      "UV",
      "UW"
    ],
    classifiedPicked: "",
    unclassifiedPicked: "",
    notes: "",
    total_request: 0.0,
    full_time: 0.0,
    inter_time: 0.0,
    hrs: 0.0,
    startLeaveDate: "",
    endLeaveDate: "",
    payrate: "",
    numWeeks: 0,
    leavePlan: [],
    leaveTypes: [
      { type: "Sick", value: "LTS" },
      { type: "Vacation", value: "LTV" },
      { type: "AAUP/SEIU", value: "LW1" },
      { type: "Short Term Disability", value: "STD" },
      { type: "Unpaid Leave", value: "LW3" },
      { type: "FLSA/NLFA", value: "LSA" },
      { type: "Personal Day", value: "Per" }
    ],
    leaveMax: [
      0.0, // LTS
      0.0, // LTV
      0.0, // LW1
      0.0, // STD
      0.0, // LW3
      0.0, // LSA
      0.0 // Per
    ],
    leaveSummary: [
      0.0, // LTS
      0.0, // LTV
      0.0, // LW1
      0.0, // STD
      0.0, // LW3
      0.0, // LSA
      0.0 // Per
    ],
    leaveStatus: [
      "FMLA-Female EE's pregnancy and care of newborn",
      "FMLA-Male EE's care of newborn",
      "FMLA-Spouse, child, parent with serious health condition",
      "FMLA-EE's own serious health condition",
      "FMLA-Newly adopted or newly place foster child",
      "FMLA-Qualifying exigency for family member in military",
      "FMLA-Wounded or ill family member in military-up to 26 wks",
      "Military Leave",
      "OFLA-Female EE disabled by pregnancy",
      "OFLA-Female EE's pregnancy and care of newborn",
      "OFLA-Spouse, child, parent with serious health condition",
      "OFLA-Male EE's care of newborn",
      "OFLA-EE's own serious health condition",
      "OFLA-Newly adopted or newly place foster child",
      "OFLA-Care for EE child sick/injured not serious hom care",
      "OFLA-Parent-in-law, grndchild, grndparent serious hlth cond",
      "OFLA-Bereavement Leave",
      "OFLA-Same-sex domestic partner serious health condition",
      "OFLA-Parent/child of sm-sx domestic ptnr serious hlth cond",
      "ADA only",
      "ADA/FMLA and/or OFLA",
      "Workers compensation only",
      "Work Comp/FMLA"
    ],
    reasons: [
      "FMLA/OFLA Continuous Concurrent Leave",
      "FMLA/OFLA Intermittent Concurrent Leave",
      "ER Administrative Leave (Employee Relations)",
      "FMLA Continuous Leave",
      "FMLA Intermittent Leave",
      "OFLA Intermittent Leave",
      "OFLA Continuous Leave",
      "Other Non-FMLA/OFLA Leave",
      "PC Pending Certification",
      "Amer. With Disabilities Act (ADA)",
      "Injured Worker (workers comp)",
      "AP Paid Administrative Leave (LW1)",
      "AU Unpaid Administrative Leave (LWOP)",
      "Discretionary Leave (intermittent)",
      "Discretionary Leave (continuous)"
    ]
  }),
  computed: {
    fmlaEligibility: function() {
      if (this.user.fmla_eligibility == "T") {
        return "Eligible";
      }
      return "Not Eligible";
    },
    oflaEligibility: function() {
      if (this.user.ofla_eligibility == "T") {
        return "Eligible";
      } else if (this.user.ofla_eligibility == "B") {
        return "Parental or Military Leave only";
      } else if (this.user.ofla_eligibility == "M") {
        return "Military Leave only";
      } else if (this.user.ofla_eligibility == "P") {
        return "Parental Leave only";
      }
      return "Not Eligible";
    },
    pathway: function() {
      var reason = [];
      for (let i = 0; i < this.user.stack.length; i++) {
        let edge = this.Nodes[this.user.stack[i].node].options[
          this.user.stack[i].edge
        ];
        let title = this.user.stack[i].node;
        reason[i] = title + ": " + edge.title;
      }
      return reason;
    },
    pd_hours: function() {
      let weeks = 0;
      if (this.user.paid_leave_balances["PD"])
        weeks += this.user.paid_leave_balances["PD"];
      console.log("wek: ", weeks);
      return 40 * this.user.fte * weeks;
    },
    max_protected_leave_hrs: function() {
      let weeks = 0;
      if (this.user.paid_leave_balances["PD"])
        weeks += this.user.paid_leave_balances["PD"];
      if (weeks) {
        return (
          this.user.fte * (weeks + 12) * 40 -
          this.user.protected_leave_hrs_taken
        );
      }
      return this.user.fte * 480 - this.user.protected_leave_hrs_taken;
    },
    std_hours: function() {
      if (this.lst) {
        if (this.pd_hours) {
          this.leaveMax[3] = this.pd_hours;
          return this.pd_hours;
        }
        /*
        TODO: check this
        else if (serious health condition self; pre-existing condition){
          this.leaveMax[3] = 40 * this.user.fte * 4;
          return 40 * this.user.fte * 4;
        }
        else if (serious health condition self; not a pre-existing health condition){
          this.leaveMax[3] = 40 * this.user.fte * 13;
          return 40 * this.user.fte * 13;
        }
        */
      }
      return 0;
    },
    pxsHours: function() {
      if (this.user.deductions_eligibility["PXS"]) {
        //TODO: get some amount?
        return 0;
      }
      return 0;
    },
    unpaid_hours: function() {
      let NoUnpaid_total = 0.0;
      for (var week in this.leavePlan) {
        if (this.leavePlan[week].leaveType !== "LW3")
          NoUnpaid_total += parseFloat(this.leavePlan[week].leaveUsed);
      }
      return this.max_protected_leave_hrs - NoUnpaid_total;
    },
    dslb: function() {
      this.leaveMax[2] += this.user.aaup ? this.user.fte * 320 : 0;
      return this.aaup ? this.user.fte * 320 : 0;
    },
    lst: function() {
      return this.user.deductions_eligibility.includes("LST");
    },
    pxs: function() {
      return this.user.deductions_eligibility.includes("PXS");
    },
    aaup: function() {
      return this.user.deductions_eligibility.includes("AAUP");
    },
    seiu: function() {
      return this.user.deductions_eligibility.includes("SEIU");
    },
    total: function() {
      let hours = 0.0;
      let pay = 0.0;
      for (var type in this.leaveSummary) {
        hours += this.leaveSummary[type];
        if (this.payrate) {
          if (this.leaveTypes[type].value === "STD") {
            pay += this.leaveSummary[type] * parseFloat(this.payrate) * 0.6;
          } else if (this.leaveTypes[type].value === "LW3") {
            pay += this.leaveSummary[type] * parseFloat(this.payrate) * 0.0;
          } else {
            pay += this.leaveSummary[type] * parseFloat(this.payrate);
          }
        }
      }
      return { hours, pay };
    },
    classifiedEmp: function() {
      for (var emp in this.classifiedEmpList) {
        if (this.user.employee_classification == this.classifiedEmpList[emp]) {
          console.log("classified");
          return true;
        }
      }
      console.log("not classified");
      return false;
    },
    unclassifiedEmp: function() {
      for (var emp in this.unclassifiedEmpList) {
        if (
          this.user.employee_classification == this.unclassifiedEmpList[emp]
        ) {
          console.log("unclassified");
          return true;
        }
      }
      console.log("not unclassified");
      return false;
    },
    vacationHours: function() {
      if (this.user.paid_leave_balances["AVAC"]) {
        if (this.classifiedPicked == "yes") {
          this.leaveMax[1] = this.user.paid_leave_balances["AVAC"] - 40;
        } else if (this.unclassifiedPicked == "yes") {
          this.leaveMax[1] = 0;
        } else if (this.user.paid_leave_balances["AVAC"]) {
          this.leaveMax[1] = this.user.paid_leave_balances["AVAC"];
        } else {
          this.leaveMax[1] = 0;
        }
        return this.leaveMax[1];
      }
      return 0;
    },
    hardshipHours: function() {
      if (this.user.paid_leave_balances["XDON"]) {
        this.leaveMax[2] += this.user.paid_leave_balances["XDON"];
        return this.user.paid_leave_balances["XDON"];
      }
      return 0;
    },
    exchangeHours: function() {
      if (this.user.paid_leave_balances["XCHG"]) {
        //TODO: which leave type does this go to?
        //this.leaveMax[] = this.user.paid_leave_balances["XDON"];
        return this.user.paid_leave_balances["XCHG"];
      }
      return 0;
    },
    nslaHours: function() {
      if (this.user.paid_leave_balances["NSLA"]) {
        this.leaveMax[5] += this.user.paid_leave_balances["NSLA"];
        return this.user.paid_leave_balances["NSLA"];
      }
      return 0;
    },
    fslaHours: function() {
      if (this.user.paid_leave_balances["FSLA"]) {
        this.leaveMax[5] += this.user.paid_leave_balances["FSLA"];
        return this.user.paid_leave_balances["FSLA"];
      }
      return 0;
    },
    personalHours: function() {
      if (this.user.paid_leave_balances["PERS"]) {
        this.leaveMax[6] = this.user.paid_leave_balances["PERS"];
        return this.user.paid_leave_balances["PERS"];
      }
      return 0;
    },
    bereavementHours: function() {
      if (this.user.paid_leave_balances["SBRV"]) {
        //TODO: which leave type does this go to?
        //this.leaveMax[] = this.user.paid_leave_balances["SBRV"];
        return this.user.paid_leave_balances["SBRV"];
      }
      return 0;
    },
    furloughHours: function() {
      if (this.user.paid_leave_balances["XFUR"]) {
        //TODO: which leave type does this go to?
        //this.leaveMax[] = this.user.paid_leave_balances["XFUR"];
        return this.user.paid_leave_balances["XFUR"];
      }
      return 0;
    },
    otherHours: function() {
      if (this.user.paid_leave_balances["XOTH"]) {
        //TODO: which leave type does this go to?
        //this.leaveMax[] = this.user.paid_leave_balances["XOTH"];
        return this.user.paid_leave_balances["XOTH"];
      }
      return 0;
    },
    sickHours: function() {
      if (this.user.paid_leave_balances["ASIC"]) {
        this.leaveMax[0] = this.user.paid_leave_balances["ASIC"];
        return this.user.paid_leave_balances["ASIC"];
      }
      return 0;
    },
    total_paid_leave: function() {
      return (
        this.sickHours +
        this.otherHours +
        this.furloughHours +
        this.bereavementHours +
        this.personalHours +
        this.fslaHours +
        this.nslaHours +
        this.exchangeHours +
        this.hardshipHours +
        this.vacationHours +
        this.std_hours +
        this.pxsHours +
        this.dslb
      );
    }
  },
  mounted: function() {
    this.showError("#payrate", this.errors.payrate.empty);
    this.showError("#leaveStart", this.errors.leaveStart.empty);
    this.showError("#leaveEnd", this.errors.leaveEnd.empty);
  },
  watch: {
    startLeaveDate: function() {
      this.checkValidDates();
    },
    endLeaveDate: function() {
      this.checkValidDates();
    },
    payrate: function() {
      this.checkValidPayrate();
    }
  },
  beforeRouteLeave(to, from, next) {
    $('[data-toggle = "tooltip"]').tooltip("dispose");
    next();
  },
  methods: {
    updateSummary() {
      this.leaveSummary = [
        0.0, // LTS
        0.0, // LTV
        0.0, // LW1
        0.0, // STD
        0.0, // LW3
        0.0, // LSA
        0.0 // Per
      ];
      console.log(this.leaveMax);
      for (var index in this.leavePlan) {
        for (var type in this.leaveSummary) {
          if (
            this.leavePlan[index].leaveType === this.leaveTypes[type].value &&
            this.leavePlan[index].leaveUsed !== ""
          ) {
            if (
              this.leavePlan[index].leaveType === "LW3" ||
              (this.leaveSummary[type] <= this.leaveMax[type] &&
                this.leaveSummary[type] +
                  parseFloat(this.leavePlan[index].leaveUsed) <=
                  this.leaveMax[type] &&
                this.leavePlan[index].leaveUsed <= 40 * this.user.fte)
            ) {
              /*if (
                this.leaveSummary[type] +
                  parseFloat(this.leavePlan[index].leaveUsed) <=
                this.leaveMax[type]
              ) {*/
              this.leaveSummary[type] += parseFloat(
                this.leavePlan[index].leaveUsed
              );
              //}
            } else {
              //TODO: highlight input box red
              console.log("highlight border red");
              console.log("max: ", this.leaveMax[type]);
              //var leaveWeek = "#leaveWeek" + index
              //this.showError(leaveWeek, this.errors.leaveHours.invalid);
            }
          }
        }
      }
    },
    addLeaveType(index) {
      this.leavePlan.splice(index, 0, Object.assign({}, this.leavePlan[index]));
    },
    removeLeaveType(index) {
      this.leavePlan.splice(index, 1);
    },
    change_hours() {
      for (var index in this.leavePlan) {
        this.leavePlan[index].leaveUsed = parseFloat(this.hrs);
      }
    },
    total_r() {
      this.total_request = 0.0;
      this.total_request =
        parseFloat(this.full_time) + parseFloat(this.inter_time);
    },
    validLeaveType(leavePlanIndex, leaveType) {
      let currentLeaveBalances = {
        LTS: 0.0,
        LTV: 0.0,
        LW1: 0.0,
        STD: 0.0,
        LW3: 0.0,
        LSA: 0.0,
        Per: 0.0
      };
      currentLeaveBalances.LTS = this.leaveMax[0] - this.leaveSummary[0];
      currentLeaveBalances.LTV = this.leaveMax[1] - this.leaveSummary[1];
      currentLeaveBalances.LW1 = this.leaveMax[2] - this.leaveSummary[2];
      currentLeaveBalances.STD = this.leaveMax[3] - this.leaveSummary[3];
      currentLeaveBalances.LW3 = this.leaveMax[4] - this.leaveSummary[4];
      currentLeaveBalances.LSA = this.leaveMax[5] - this.leaveSummary[5];
      currentLeaveBalances.Per = this.leaveMax[6] - this.leaveSummary[6];

      if (this.lst) {
        if (this.leavePlan[leavePlanIndex].week == 1) {
          if (currentLeaveBalances.LTS > 0) {
            return leaveType === "LTS";
          } else if (currentLeaveBalances.LTV > 0) {
            return leaveType === "LTV";
          } else {
            return leaveType !== "STD";
          }
        } else if (
          this.leavePlan[leavePlanIndex].week <= 9 &&
          currentLeaveBalances.STD > 0
        ) {
          return leaveType === "STD";
        } else {
          if (currentLeaveBalances.LTS > 0.0) {
            return leaveType === "LTS";
          } else if (currentLeaveBalances.LTV > 0.0) {
            return leaveType === "LTV";
          } else if (leaveType === "LW1") {
            if (currentLeaveBalances["LW1"] == 0) {
              return false;
            } else {
              return true;
            }
          } else if (leaveType === "LSA") {
            if (currentLeaveBalances["LSA"] == 0) {
              return false;
            } else {
              return true;
            }
          } else if (leaveType === "Per") {
            if (currentLeaveBalances["Per"] == 0) {
              return false;
            } else {
              return true;
            }
          } else if (leaveType === "LW3") {
            if (
              currentLeaveBalances["Per"] == 0 &&
              currentLeaveBalances["LSA"] == 0 &&
              currentLeaveBalances["LW1"] == 0
            ) {
              return true;
            } else {
              return false;
            }
          } else if (leaveType === "STD") {
            return false;
          }
        }
      } else {
        if (currentLeaveBalances.LTS > 0.0) {
          return leaveType === "LTS";
        } else if (currentLeaveBalances.LTV > 0.0) {
          return leaveType === "LTV";
        } else if (leaveType === "LW1") {
          if (currentLeaveBalances["LW1"] == 0) {
            return false;
          } else {
            return true;
          }
        } else if (leaveType === "LSA") {
          if (currentLeaveBalances["LSA"] == 0) {
            return false;
          } else {
            return true;
          }
        } else if (leaveType === "Per") {
          if (currentLeaveBalances["Per"] == 0) {
            return false;
          } else {
            return true;
          }
        } else if (leaveType === "LW3") {
          if (
            currentLeaveBalances["Per"] == 0 &&
            currentLeaveBalances["LSA"] == 0 &&
            currentLeaveBalances["LW1"] == 0
          ) {
            return true;
          } else {
            return false;
          }
        } else if (leaveType === "STD") {
          return false;
        }
      }
    },
    setNumWeeks() {
      var duration = moment.duration(
        moment(this.endLeaveDate).diff(moment(this.startLeaveDate))
      );
      var numWeeks = duration.asWeeks();

      // Add missing weeks
      for (let index = this.numWeeks; index < numWeeks; index++) {
        this.leavePlan.push({ week: index + 1, leaveType: "", leaveUsed: 0.0 });
      }
      // Remove extra weeks
      for (let index = this.leavePlan.length - 1; index >= numWeeks; index--) {
        // TODO: handle multiple leavetypes for removed weeks
        if (this.leavePlan[index].week > numWeeks) this.leavePlan.pop();
        else break;
      }
      this.numWeeks = Math.ceil(numWeeks);
    },

    paid_percent(type) {
      if (type == "STD") return 60;
      else if (type == "LW3") return 0;
      return 100;
    },
    protect(week, type) {
      //TODO: re-evaluate
      let protect_total = 0.0;
      for (let weekIndex = 0; weekIndex <= week; weekIndex++) {
        if (type !== "") {
          if (this.leavePlan[weekIndex].leaveType === type) {
            protect_total += parseFloat(this.leavePlan[weekIndex].leaveUsed);
          }
        }
      }
      if (
        type === "LTS" &&
        (protect_total > this.leaveMax[0] || !this.leaveMax[0])
      ) {
        return "No";
      } else if (
        type === "LTV" &&
        (protect_total > this.leaveMax[1] || !this.leaveMax[1])
      ) {
        return "No";
      } else if (
        type === "Per" &&
        (protect_total > this.leaveMax[6] || !this.leaveMax[6])
      ) {
        return "No";
      } else if (
        type === "LSA" &&
        (protect_total > this.leaveMax[5] || !this.leaveMax[5])
      ) {
        return "No";
      } else if (type === "LW1" && protect_total > this.leaveMax[2]) {
        return "No";
      } else if (type === "LW3" && protect_total > this.unpaid_hours) {
        return "No";
      } else {
        return "Yes";
      }
    },
    showError: function(id, title) {
      $(id)
        .addClass("error")
        .tooltip("dispose")
        .attr("title", title)
        .tooltip("show");
    },
    removeError: function(ids) {
      $(ids)
        .removeClass("error")
        .tooltip("dispose")
        .attr("title", "");
    },
    checkValidPayrate() {
      if (!this.payrate) {
        this.showError("#payrate", this.errors.payrate.empty);
      } else {
        this.removeError("#payrate");
      }
    },
    // When the start and end dates are changed, this function will be called.
    // If the dates are invalid, a tooltip will appear informing the user.
    checkValidDates() {
      let startDate = moment(this.startLeaveDate);
      let endDate = moment(this.endLeaveDate);
      let today = moment();
      if (!this.startLeaveDate) {
        this.showError("#leaveStart", this.errors.leaveStart.empty);
      } else if (startDate <= today) {
        this.showError("#leaveStart", this.errors.leaveStart.past);
      } else if (!this.endLeaveDate) {
        this.removeError("#leaveStart");
      }

      if (!this.endLeaveDate) {
        this.showError("#leaveEnd", this.errors.leaveEnd.empty);
      } else if (!this.startLeaveDate || startDate <= today) {
        this.removeError("#leaveEnd");
      } else if (startDate > today) {
        if (startDate < endDate) {
          this.removeError("#leaveStart, #leaveEnd");
          this.setNumWeeks();
        } else {
          this.showError("#leaveStart", this.errors.leaveStart.invalid);
          this.showError("#leaveEnd", this.errors.leaveEnd.invalid);
        }
      }
    },
    pay(leavePlanElement) {
      if (leavePlanElement.leaveUsed) {
        if (this.payrate) {
          let pay =
            parseFloat(leavePlanElement.leaveUsed) * parseFloat(this.payrate);
          if (leavePlanElement.leaveType === "STD") {
            return "$" + (pay * 0.6).toFixed(2);
          } else if (leavePlanElement.leaveType === "LW3") {
            return "$" + (pay * 0).toFixed(2);
          } else {
            return "$" + pay.toFixed(2);
          }
        } else {
          return leavePlanElement.leaveUsed + "hrs * payrate";
        }
      } else {
        return "";
      }
    }
  }
};
</script>
<style>
.error {
  border: 1px solid red;
}
</style>
