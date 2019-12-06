<!--
 Here are a list of things that will need to be saved for each report on the db:
 - The `startLeaveDate` and `endLeaveDate` values
 - The `leavePlan` array
 - The `notes` value

 Here is a list of features that still need to be implemented:
 - parental can't use intermittent (without permission, thus should just be a warning)
 - std leave can't use intermitent
 - warn user of submitting report with unprotected leave
-->
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
          <!-- TODO possibly remove since this is shown in the leave summary -->
          <b>Total Leave Request: {{ total.hours }}</b>
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
            <!-- TODO same considerations as for `Full Time Leave` and `Intermittent Leave` row below -->
            <label for="hrWeek" class="input-group-text">HR/Week:</label>
          </div>
          <input type="text" id="hrWeek" class="form-control" />
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
      <!-- TODO possibly remove since this appears to have originally been used to estimate
          the leave summary in the excel document with the HR/Week field.  Alternatively, this
      should be done in `computed` rather than having textboxes-->
      <tr class="form-group">
        <td class="input-group">
          <div class="input-group-prepend">
            <label for="fullTime" class="input-group-text">Full Time Leave:</label>
          </div>
          <input class="form-control" type="text" id="fullTime" />
        </td>
        <td class="input-group">
          <div class="input-group-prepend">
            <label for="interTime" class="input-group-text">Intermittent Leave:</label>
          </div>
          <input class="form-control" type="text" id="interTime" />
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
      <tr
        v-for="(leavePlanElement, index) in leavePlan"
        :key="index"
        :id="'leavePlan-' + index"
        data-toggle="tooltip"
        data-trigger="manual"
      >
        <td v-if="index===0||leavePlanElement.week!==leavePlan[index-1].week">
          <button
            @click="addLeaveType(index) || updateSummary()"
            class="btn btn-info"
          >Add Leave Type</button>
        </td>
        <td v-else>
          <button
            @click="removeLeaveType(index) || updateSummary()"
            class="btn btn-danger"
          >Remove Leave Type</button>
        </td>
        <td>&nbsp;{{ leavePlanElement.week }}</td>
        <td>&nbsp;{{ is_protected(index,leavePlanElement.leaveType) ? "Yes" : "No" }}</td>
        <td>
          <select v-model="leavePlanElement.leaveType" @click="updateSummary" class="form-control">
            <option
              v-for="value of Object.keys(leaveTypes)"
              :value="value"
              :key="value"
              :disabled="!validLeaveType(index, value)"
            >{{ leaveTypes[value] }}</option>
          </select>
        </td>
        <td>&nbsp;{{ paid_percent(leavePlanElement.leaveType) * 100 }}%</td>
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
      <tr v-for="type of Object.keys(leaveSummary)" :key="type">
        <td>{{ leaveTypes[type] }}</td>
        <td>{{ leaveSummary[type] }}</td>
        <td>${{ (leaveSummary[type] * payrate * paid_percent(type)).toFixed(2) }}</td>
      </tr>
      <tr>
        <td>
          <h4>Total</h4>
        </td>
        <td>
          <h4>{{ total.hours }}</h4>
        </td>
        <td>
          <h4>${{ total.pay.toFixed(2) }}</h4>
        </td>
      </tr>
      <tr>
        <button class="btn btn-success" @click="saveAsNewReport">Save As New Report</button>
        <button class="btn btn-success" @click="saveReport">Update Report</button>
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
// Used for date comparisons, and getting the number of weeks between two dates
import moment from "moment";
// Used for displaying and removing Bootstrap tooltips manually
import $ from "jquery";
// Needed for Bootstrap tooltips
// TODO look into using BootstrapVue tooltips instead
import "bootstrap";
export default {
  name: "report",
  props: ["user", "auth", "report", "report-id", "Nodes"],
  data: () => ({
    // The various error messages that will appear in Boostrap tooltips when relevant
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
    // The classified employee types that are compared to `user.employee_classification`
    classifiedEmpList: ["CA", "CB", "CD", "CE", "GI", "GJ"],
    // The unclassified employee types that are compared to `user.employee_classification`
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
    // The v-model value set from conditionally rendered radio buttons,
    // set to 'yes' or 'no' by a classified employee as to whether or not
    // they want to hold 40hrs of vacation time
    classifiedPicked: "",
    // The v-model value set from conditionally rendered radio buttons,
    // set to 'yes' or 'no' by an unclassified employee as to whether or not
    // they want to save their vacation hours
    unclassifiedPicked: "",
    // The v-model value from the Notes textarea
    notes: "",
    // The start date of the leave being submitted
    startLeaveDate: "",
    // The end date of the leave being submitted
    endLeaveDate: "",
    // The $/hr provided by the employee
    payrate: "",
    // The number of weeks between the start and end dates
    numWeeks: 0,
    // The array of objects representing the leave plan table; which each holds a leave type, and number of hours used
    leavePlan: [],
    // The different leave types that exist
    leaveTypes: {
      LTS: "Sick",
      LTV: "Vacation",
      LW1: "AAUP/SEIU",
      STD: "Short Term Disability",
      LW3: "Unpaid Leave",
      LSA: "FLSA/NLFA",
      Per: "Personal Day"
    },
    leaveMax: {
      LTS: 0.0,
      LTV: 0.0,
      LW1: 0.0,
      STD: 0.0,
      LW3: 0.0,
      LSA: 0.0,
      Per: 0.0
    },
    // The summary of the number of hours used for each leave type within `leavePlan`
    // Is updated in the `updateSummary` method
    leaveSummary: {
      LTS: 0.0,
      LTV: 0.0,
      LW1: 0.0,
      STD: 0.0,
      LW3: 0.0,
      LSA: 0.0,
      Per: 0.0
    },
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
      if (this.user.fmla_eligibility === "T") {
        return "Eligible";
      }
      return "Not Eligible";
    },
    oflaEligibility: function() {
      switch (this.user.ofla_eligibility) {
        case "T":
          return "Eligible";
        case "B":
          return "Parental or Military Leave only";
        case "M":
          return "Military Leave only";
        case "P":
          return "Parental Leave only";
        default:
          return "Not Eligible";
      }
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
          this.leaveMax.STD = this.pd_hours;
          return this.pd_hours;
        }
        /*
        TODO: check this
        else if (serious health condition self; pre-existing condition){
          this.leaveMax.STD = 40 * this.user.fte * 4;
          return 40 * this.user.fte * 4;
        }
        else if (serious health condition self; not a pre-existing health condition){
          this.leaveMax.STD = 40 * this.user.fte * 13;
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
      this.leaveMax.LW3 = this.max_protected_leave_hrs - NoUnpaid_total;
      return this.leaveMax.LW3;
    },
    dslb: function() {
      this.leaveMax.LW1 += this.user.aaup ? this.user.fte * 320 : 0;
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
      for (const type of Object.keys(this.leaveSummary)) {
        hours += this.leaveSummary[type];
        if (this.payrate) {
          pay +=
            this.leaveSummary[type] *
            parseFloat(this.payrate) *
            this.paid_percent(type);
        }
      }
      return { hours, pay };
    },
    classifiedEmp: function() {
      return this.classifiedEmpList.includes(this.user.employee_classification);
    },
    unclassifiedEmp: function() {
      return this.unclassifiedEmpList.includes(
        this.user.employee_classification
      );
    },
    vacationHours: function() {
      if (this.classifiedPicked === "yes") {
        this.leaveMax.LTV = this.user.paid_leave_balances["AVAC"] - 40;
      } else if (this.unclassifiedPicked === "yes") {
        this.leaveMax.LTV = 0;
      } else if (this.user.paid_leave_balances["AVAC"]) {
        this.leaveMax.LTV = this.user.paid_leave_balances["AVAC"];
      } else {
        this.leaveMax.LTV = 0;
      }
      return this.leaveMax.LTV;
    },
    hardshipHours: function() {
      if (this.user.paid_leave_balances["XDON"]) {
        this.leaveMax.LW1 += this.user.paid_leave_balances["XDON"];
        return this.user.paid_leave_balances["XDON"];
      }
      return 0;
    },
    exchangeHours: function() {
      if (this.user.paid_leave_balances["XCHG"]) {
        //TODO: which leave type does this go to?
        //this.leaveMax[] = this.user.paid_leave_balances["XCHG"];
        return this.user.paid_leave_balances["XCHG"];
      }
      return 0;
    },
    nslaHours: function() {
      if (this.user.paid_leave_balances["NSLA"]) {
        this.leaveMax.LSA += this.user.paid_leave_balances["NSLA"];
        return this.user.paid_leave_balances["NSLA"];
      }
      return 0;
    },
    fslaHours: function() {
      if (this.user.paid_leave_balances["FSLA"]) {
        this.leaveMax.LSA += this.user.paid_leave_balances["FSLA"];
        return this.user.paid_leave_balances["FSLA"];
      }
      return 0;
    },
    personalHours: function() {
      if (this.user.paid_leave_balances["PERS"]) {
        this.leaveMax.Per = this.user.paid_leave_balances["PERS"];
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
        this.leaveMax.LTS = this.user.paid_leave_balances["ASIC"];
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
    let B = {};
    console.log("FOO: " + this.report);
    //if(this.report != "") {
    B = JSON.parse(this.report);
    this.leavePlan = B.leavePlan;
    for (var week in this.leavePlan) {
      for (var type in this.leaveSummary) {
        if (this.leavePlan[week].leaveType === this.leaveSummary[type].name) {
          if (this.leavePlan[week].hasOwnProperty("hours")) {
            this.leaveSummary[type].hours += parseFloat(
              this.leavePlan[week].leaveUsed
            );
          }
        }
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

    this.payrate = B.payrate;
    this.leaveSummary = B.summary;
    this.user.stack = B.stack;
    this.endLeaveDate = B.endLeaveDate;
    this.startLeaveDate = B.startLeaveDate;
    //}
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
      this.leaveSummary = {
        LTS: 0.0,
        LTV: 0.0,
        LW1: 0.0,
        STD: 0.0,
        LW3: 0.0,
        LSA: 0.0,
        Per: 0.0
      };
      console.log("maths: ", 0 + 0);
      console.log("maths: ", 0 + 0.0);
      console.log("maths: ", 0.0 + 0.0);
      for (var index in this.leavePlan) {
        for (const type of Object.keys(this.leaveSummary)) {
          if (
            this.leavePlan[index].leaveType === type &&
            this.leavePlan[index].leaveUsed !== ""
          ) {
            //Check if the input hours exceed that type's max hours
            if (
              this.leavePlan[index].leaveType === "LW3" ||
              (this.leaveSummary[type] <= this.leaveMax[type] &&
                this.leaveSummary[type] +
                  parseFloat(this.leavePlan[index].leaveUsed) <=
                  this.leaveMax[type] &&
                this.leavePlan[index].leaveUsed <= 40 * this.user.fte)
            ) {
              //Check if combined leaves for that week exceed max weekly hours: 40 * this.user.fte
              var thisWeeksHours = 0;
              for (var plan in this.leavePlan) {
                if (this.leavePlan[plan].week === this.leavePlan[index].week) {
                  thisWeeksHours += parseFloat(this.leavePlan[plan].leaveUsed);
                }
              }
              if (thisWeeksHours <= 40 * this.user.fte) {
                //If everything is good, add it to our plan and get rid of any error messages
                this.leaveSummary[type] += parseFloat(
                  this.leavePlan[index].leaveUsed
                );
                this.removeError("#leavePlan-" + index);
              } else {
                this.showError(
                  "#leavePlan-" + index,
                  this.errors.leaveHours.invalid
                );
              }
            } else {
              this.showError(
                "#leavePlan-" + index,
                this.errors.leaveHours.invalid
              );
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
    validLeaveType(leavePlanIndex, leaveType) {
      let currentLeaveBalances = {
        LTS: this.leaveMax.LTS - this.leaveSummary.LTS,
        LTV: this.leaveMax.LTV - this.leaveSummary.LTV,
        LW1: this.leaveMax.LW1 - this.leaveSummary.LW1,
        STD: this.leaveMax.STD - this.leaveSummary.STD,
        LW3: this.leaveMax.LW3 - this.leaveSummary.LW3,
        LSA: this.leaveMax.LSA - this.leaveSummary.LSA,
        Per: this.leaveMax.Per - this.leaveSummary.Per
      };

      if (this.lst) {
        if (this.leavePlan[leavePlanIndex].week === 1) {
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
            return currentLeaveBalances["LW1"] !== 0;
          } else if (leaveType === "LSA") {
            return currentLeaveBalances["LSA"] !== 0;
          } else if (leaveType === "Per") {
            return currentLeaveBalances["Per"] !== 0;
          } else if (leaveType === "LW3") {
            return (
              currentLeaveBalances["Per"] === 0 &&
              currentLeaveBalances["LSA"] === 0 &&
              currentLeaveBalances["LW1"] === 0
            );
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
          return currentLeaveBalances["LW1"] !== 0;
        } else if (leaveType === "LSA") {
          return currentLeaveBalances["LSA"] !== 0;
        } else if (leaveType === "Per") {
          return currentLeaveBalances["Per"] !== 0;
        } else if (leaveType === "LW3") {
          return (
            currentLeaveBalances["Per"] === 0 &&
            currentLeaveBalances["LSA"] === 0 &&
            currentLeaveBalances["LW1"] === 0
          );
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
    // Returns the paid percentage for the given leave type as a value between 0.0-1.0
    paid_percent(type) {
      switch (type) {
        case "STD":
          return 0.6;
        case "LW3":
          return 0.0;
        default:
          return 1.0;
      }
    },
    saveAsNewReport() {
      //This function will allow admin/user to save a copy of the report
      //they are working on, preserving the current report
      var data = JSON.stringify({
        EMPLOYEE_ID: this.user.employee_id,
        REPORT: {
          leavePlan: this.leavePlan,
          payrate: this.payrate,
          summary: this.leaveSummary,
          stack: this.user.stack,
          startLeaveDate: this.startLeaveDate,
          endLeaveDate: this.endLeaveDate
        }
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
    },
    is_protected(index, type) {
      //Will check to see if adding this week will exceed the protected leave limit
      let protect_total = 0.0;
      for (let evaluatedIndex = 0; evaluatedIndex <= index; evaluatedIndex++) {
        if (type !== "") {
          protect_total += parseFloat(this.leavePlan[evaluatedIndex].leaveUsed);
        }
      }
      if (protect_total > this.max_protected_leave_hrs) {
        return false;
      } else {
        return true;
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
    saveReport() {
      //This function will allow admin/user to save the new updates of
      //the report they are working on to itself

      var tosend = JSON.stringify({
        REPORT_ID: this.reportId,
        EMPLOYEE_ID: this.user.employee_id,
        REPORT: {
          leavePlan: this.leavePlan,
          payrate: this.payrate,
          summary: this.leaveSummary,
          stack: this.user.stack,
          startLeaveDate: this.startLeaveDate,
          endLeaveDate: this.endLeaveDate
        }
      });
      console.log(tosend);
      fetch("http://localhost:8000/database/updatereport/", {
        method: "POST",
        body: tosend,
        headers: {
          "Content-Type": "application/json",
          Authorization: this.auth
        }
      });
      this.$emit("update-employee");
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
