<template>
  <div id="questions" class="container">
    <div v-if="isAdmin" class="row">
      <div class="input-group mb-3 col-md-3">
        <div class="input-group-prepend">
          <span class="input-group-text">Run as: </span>
        </div>
        <input
          type="text"
          placeholder="other username"
          class="form-control"
          v-model="usrname"
        />
      </div>
      <div class="col-md-2">
        <button class="btn btn-success" @click="changeUser">Change User</button>
      </div>
    </div>
    <btn-question
      :title="currentNode"
      :options="Nodes[currentNode].options"
      @option-selected="optionSelected"
      v-if="Nodes[currentNode].input === 'button'"
    ></btn-question>

    <display-question
      :title="currentNode"
      :options="Nodes[currentNode].options"
      @option-selected="optionSelected"
      v-else-if="Nodes[currentNode].input === 'display'"
    ></display-question>

    <drop-down-question
      :title="currentNode"
      :options="Nodes[currentNode].options"
      @option-selected="optionSelected"
      v-else-if="Nodes[currentNode].input === 'drop down'"
    ></drop-down-question>

    <btn-question
      :title="currentNode"
      :options="Nodes[currentNode].options"
      @option-selected="optionSelected"
      v-if="Nodes[currentNode].input === 'database'"
    ></btn-question>

    <!-- <database-question :title="currentNode" :options="Nodes[currentNode].options"
       @option-selected="optionSelected" v-else-if="Nodes[currentNode].input == 'database'"></database-question> -->
    <br />
    <button class="btn btn-success" @click="goBack()" v-if="stack[0]">
      Back
    </button>
  </div>
</template>

<script>
import BtnQuestion from "./BtnQuestion.vue";
import DisplayQuestion from "./DisplayQuestion.vue";
import DropDownQuestion from "./DropDownQuestion.vue";
import DatabaseQuestion from "./DatabaseQuestion.vue";

export default {
  name: "questions",
  props: ["isAdmin", "user"],
  data: () => ({
    currentNode: "Do you have a work related injury?",
    hours: 0,
    stack: [],
    usrname: "",
    Nodes: {
      "Do you have a work related injury?": {
        input: "button",
        options: [
          {
            title: "Yes",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Talk to Jack"
          },
          {
            title: "No",
            next_node: "Qualified (Employee Status)",
            add_hours: {
              hours: 0,
              type: "n/a"
            }
          },
          {
            title: "More Info",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Work Related Injury Info"
          }
        ]
      },
      "Qualified (Employee Status)": {
        input: "database",
        options: [
          {
            title: "Yes, OFLA (minimum)",
            next_node: "What is your reason for requesting leave?",
            add_hours: {
              hours: 0,
              type: "n/a"
            }
          },
          {
            title: "Yes, only ADA ",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "You are only entitled for ADA: Is it a Disability?"
          }
        ]
      },
      "What is your reason for requesting leave?": {
        input: "button",
        options: [
          {
            title: "Serious Health Condition Family",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Serious Health Condition Family"
          },
          {
            title: "Serious Health Condition Self",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Serious Health Condition Self"
          },
          {
            title: "Pregnancy Disability",
            next_node: "Pregnancy Disability",
            add_hours: {
              hours: 0,
              type: "n/a"
            }
          },
          {
            title: "Parental Leave",
            next_node: "Which type of Parental leave are you requesting?",
            add_hours: {
              hours: 0,
              type: "n/a"
            }
          },
          {
            title: "Military leave",
            next_node: "Talk to Jack",
            add_hours: {
              hours: 0,
              type: "n/a"
            }
          },
          {
            title: "Other",
            next_node: "Talk to Jack",
            add_hours: {
              hours: 0,
              type: "n/a"
            }
          }
        ]
      },
      "Work Related Injury Info": {
        input: "display",
        options: [
          {
            title:
              "If an employee experiences an accidental injury, or occupational disease that qualifies for workers' compensation protections, medical and/or time loss benefits may be available through SAIF Corporation.\n Injuries must be reported, even if you do not seek medical treatment.\n More info: https://www.pdx.edu/hr/workers-compensation ",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: ""
          }
        ]
      },
      "You are only entitled for ADA: Is it a Disability?": {
        input: "button",
        options: [
          {
            title: "Information on Qualifying Disabilities",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Disability Info"
          },
          {
            title: "Information ADA",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "ADA Info"
          },
          {
            title: "Yes need to add link to ADA form",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Talk to Jack"
          },
          {
            title: "No",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Exceptions"
          }
        ]
      },
      "Serious Health Condition Family": {
        input: "button",
        options: [
          {
            title: "Description of Serious Health Condition",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Description of Serious Health Condition"
          },
          {
            title: "Continue",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node:
              "Which Family member is suffering a serious health condition?"
          }
        ]
      },
      "Serious Health Condition Self": {
        input: "button",
        options: [
          {
            title: "Continue",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "List of Serious Health Conditions"
          }
        ]
      },
      "Description of Serious Health Condition": {
        input: "display",
        options: [
          {
            title:
              "A serious health condition is an illness, injury, impairment, or physical or mental condition that incapacitates you or an eligible family member for 3 consecutive days or longer, and involves at least one of the following: \n Hospital care, \n Absence plus treatment, \n Pregnancy, \n Chronic conditions, \n Permanent/Long-term conditions requiring supervision, \n Multiple treatments (Non-chronic conditions), \n Important definitions for understanding what qualifies as a serious health conditions include: \n ,Incapacity: the inability to work, attend school or perform other regular daily activities due to a serious health condition or treatment for or recovery from a serious health condition , \n Treatment: includes examinations to determine if a serious health condition exists and evaluations of the condition. It does not include routine physical examinations, eye examinations or dental examinations",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Description of serious health condition"
          }
        ]
      },
      "List of Serious Health Conditions": {
        input: "drop down",
        options: [
          {
            title: "Description of Serious Health Condition",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Description of Serious Health Condition"
          },
          {
            title:
              "Hospital care:  Inpatient care (i.e., an overnight stay) in a hospital, hospice, or residential medical care facility, including any period of incapacity or subsequent treatment in connection with or as a consequence of inpatient care.",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Report"
          },
          {
            title:
              "Absence plus treatment:  A period of incapacity of more than three consecutive calendar days, including any subsequent treatment or period of incapacity relating to the same condition, that also involves: Two or more treatments by a health care provider, nurse or physician's assistant under the direct supervision of a health care provider, or by a provider of health care services (e.g., physical therapist) under the orders of, or on referral by, a health care provider; or One treatment by a health care provider which results in a regimen of continuing treatment under the supervision of a healthcare provider.",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Report"
          },
          {
            title:
              "Pregnancy: Any period of incapacity for pregnancy-related disabilities or illnesses, or for prenatal care..",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Report"
          },
          {
            title:
              "Chronic conditions: A chronic condition exists when the condition: Requires at least 2 visits a year for treatment by health care provider or by a nurse or physician's assistant under the direct supervision of a health care provider; Continues over an extended period of time (including recurring episodes of a single underlying condition); andMay cause episodic rather than a continuing period of incapacity (e.g., asthma, diabetes, epilepsy).",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Report"
          },
          {
            title:
              "Permanent/Long-term conditions requiring supervision: A period of incapacity that is permanent or long-term due to a condition for which treatment is potentially ineffective. The employee or family member is under the supervision of a health care provider, not necessarily receiving active treatment. Examples include Alzheimer's disease, a severe stroke, or the terminal stages of a disease",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Report"
          },
          {
            title:
              "Multiple treatments (Non-chronic conditions): Any period of absence to receive multiple treatments (including any period of recovery time) by a health care provider or by a provider of health care services under the orders of, or on referral by, a health care provider, either for restorative surgery after an accident or other injury, or for a condition that would likely result in a period of incapacity of more than three consecutive calendar days in the absence of medical intervention or treatment, such as cancer (chemotherapy, radiation, etc.), severe arthritis (physical therapy), and kidney disease (dialysis). ",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Report"
          }
        ]
      },
      "Talk to Jack": {
        input: "display",
        options: [
          {
            title: "Please call Jack ***-***-**** or Email: jack@pdx.edu",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: ""
          }
        ]
      },
      "Disability Info": {
        input: "display",
        options: [
          {
            title:
              "An individual with a disability is a person who: \n Has a physical or mental impairment that substantially limits one or more major life activities; \n Has a record of such impairment; or \n Is regarded as having such an impairment \n Under the ADAAA (ADA Amendments Act) Major life Activities now additionally includes Major Bodily Functions. In total a disability would be any impairment that substantially limits any of the following: Major life activities include, but are not limited to, caring for oneself, performing manual tasks, seeing, hearing, eating, sleeping, walking, standing, lifting, bending, speaking, breathing, learning, reading, concentrating, thinking, communicating, and working. Major Bodily Functions include, but are not limited to, functions of the immune system, normal cell growth, digestive, bowel, bladder, neurological, brain, respiratory, circulatory, endocrine, and reproductive functions. \n The term “substantially limits” should be construed broadly in favor of expansive coverage to the maximum extent permitted by the terms of the ADA. The primary focus of the ADA is on whether discrimination occurred, the determination of disability should not require extensive analysis. \n A qualified employee or applicant with a disability is an individual who, with or without reasonable accommodation, can perform the essential functions of the job in question \n Please note that HR will never disclose and a supervisor should never discuss or request disability-specific medical information. The employee's privacy will be maintained at all times. All medical certification and any determination of an underlying disability will be performed exclusively by HR. \n More info: https://www.pdx.edu/hr/employee-accommodations ",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Description of serious health condition"
          }
        ]
      },
      "Which Family member is suffering a serious health condition?": {
        input: "button",
        options: [
          {
            title:
              "Spouse: as recognized under any state or foreign jursidiction, or registered same-sex domestic partner",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "List of Serious Health Conditions"
          },
          {
            title:
              "Son or Daughter: biological, adopted, foster or stepchild, a legal ward, child of whom the employee stands “in loco parentis”, or a child of the employee’s same-sex domestic partner of any age",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "List of Serious Health Conditions"
          },
          {
            title:
              "Parent: biological or adoptive mother or father, or an individual who is “in loco parentis” (in place of a parent), and the parent of the employee’s spouse or same-sex partner",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "List of Serious Health Conditions"
          },
          {
            title: "Grandparent or grandchild",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "List of Serious Health Conditions"
          },
          {
            title: "None of the above",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "You do not qualify for protected leave"
          }
        ]
      },
      "Which type of Parental leave are you requesting?": {
        input: "button",
        options: [
          {
            title: "Sick Child (not serious)",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Report"
          },
          {
            title: "Parental (not pregnant)",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Report"
          }
        ]
      },
      Report: {
        input: "button",
        options: [
          {
            title: "route to report",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "n/a"
          }
        ]
      },
      "Pregnancy Disability": {
        input: "button",
        options: [
          {
            title: "C-Section",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Report"
          },
          {
            title: "Vaginal Birth",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Report"
          }
        ]
      },
      "ADA Info": {
        input: "display",
        options: [
          {
            title:
              "Title I of the Americans with Disabilities Act of 1990 prohibits private employers, state and local governments, employment agencies and labor unions from discriminating against qualified individuals with disabilities in job application procedures, hiring, firing, advancement, compensation, job training, and other terms, conditions, and privileges of employment. Briefly Title I of the ADA \n Helps people with disabilities access the same employment opportunities and benefits available to people without disabilities. \n Applies to employers with 15 or more employees. \n Requires employers to provide reasonable accommodations to qualified applicants or employees. A “reasonable accommodation” is a change that accommodates employees with disabilities so they can do the job without causing the employer “undue hardship” (too much difficulty or expense). \n Defines disability, establishes guidelines for the reasonable accommodation process, and addresses medical examinations and inquiries. \n Regulated and enforced by the U.S. Equal Employment Opportunity Commission. ",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "n/a"
          }
        ]
      },
      Exceptions: {
        input: "button",
        options: [
          {
            title: "Under 6 months",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Are You Requesting Military Leave?"
          },
          {
            title: "Over 6 months, but less than 650 hours and 520 hrs or more",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Are You Requesting Military Leave or Parental Leave?"
          },
          {
            title: "Over 6 months but less than 520 hrs",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Are You Requesting Parental Leave?"
          }
        ]
      },
      "Are You Requesting Military Leave?": {
        input: "button",
        options: [
          {
            title: "Yes",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Talk to Jack"
          },
          {
            title: "No",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "You do not qualify for protected leave"
          }
        ]
      },
      "Are You Requesting Military Leave or Parental Leave?": {
        input: "button",
        options: [
          {
            title: "Parental Leave",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Which type of Parental leave are you requesting?"
          },
          {
            title: "Military Leave",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Talk to Jack"
          },
          {
            title: "None of The Above",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "You do not qualify for protected leave"
          }
        ]
      },
      "Are You Requesting Parental Leave?": {
        input: "button",
        options: [
          {
            title: "Yes",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Which type of Parental leave are you requesting?"
          },
          {
            title: "No",
            weeks: 0,
            next_node: "You do not qualify for protected leave"
          }
        ]
      },
      "You do not qualify for protected leave": {
        input: "button",
        options: [
          {
            title:
              "Your employee type does not receive protected leave \n You have not accumulated enough working hours to qualify \n You have not worked for the required length of time to qualify",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "n/a"
          },
          {
            title:
              "If you feel this answer is not correct, please contact Jack Dorkey",
            add_hours: {
              hours: 0,
              type: "n/a"
            },
            next_node: "Talk to Jack"
          }
        ]
      }
    }
  }),
  computed: {},
  components: {
    BtnQuestion,
    DisplayQuestion,
    DropDownQuestion,
    DatabaseQuestion
  },
  methods: {
    optionSelected(selected) {
      console.log(selected);
      //do any relevant stuff here ie addWeeks
      let curr = this.Nodes[this.currentNode].options[selected];
      if (curr.weeks !== 0) {
        this.$emit("add-weeks", curr.weeks);
      }

      this.stack.push(this.currentNode);
      this.currentNode = curr.next_node;
    },
    goBack() {
      console.log("in go back");
      let oldNode = this.currentNode;
      this.currentNode = this.stack.pop();
      //logic to find Nodes[currentNod] option leading to oldNode
      // then update weeks if needed
        let option;
        //Find the path from the node we backed up to, to the one we left
        for (let o in this.Nodes[this.currentNode].options) {
            if (o.next_node === oldNode) {
                option = o;
                break;
            }
        }
        //If this edge modifies the number of protected weeks, undo that change because
        //we are backing up
        if(option.hasOwnProperty('weeks')){
            this.$emit('add-weeks', -option.weeks);
        }
    },
    changeUser() {
      //add code to replace the user object with a new one based on a provided username
      console.log(this.usrname);
    }
  }
};
</script>
<!-- styling for the component -->
<style>
#questions {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
