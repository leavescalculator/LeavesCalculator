<template>
  <div id="questions">
    Questions Page!
    <btn-question :title="currentNode" :options="Nodes[currentNode].options" 
      @option-selected="optionSelected"></btn-question>
  </div>
</template>

<script>
import BtnQuestion from './BtnQuestion.vue';

export default {
  name: 'questions',
  data: () => ({
    currentNode: "Do you have a work related injury?",
    hours: 0,
    Nodes: {
    "Do you have a work related injury?": {
      "input": "button",
      "options": [
        {
          "title": "Yes",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Workers comp"
        },
        {
          "title": "no",
          "next_node": "Qualified (Employee Status)",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          }
        }
      ]
    },
    "Qualified (Employee Status)": {
      "input": "database",
      "options": [
        {
          "title": "Yes, OFLA (minimum)",
          "next_node": "What is your reason for requesting leave?",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          }
        },
        {
          "title": "Yes, only ADA ",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "You are only entitled for ADA: Is it a Disability?"
        },
        {
          "title": "no",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Talk to Jack"
        }
      ]
    },
    "Workers comp": {
      "input": "Display",
      "options": [
        {
          "title": "Is this for woker's comp?",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Talk to Jack"
        }
      ]
    },
    "What is your reason for requesting leave?": {
      "input": "button",
      "options": [
        {
          "title": "Serious Health Condition Family",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Serious Health Condition Family"
        },
        {
          "title": "Serious Health Condition Self",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Serious Health Condition Self"
        },
        {
          "title": "Pregnancy Disability",
          "next_node": "Parental Leave",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          }
        },
        {
          "title": "Parental Leave",
          "next_node": "Parental Leave",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          }
        },
        {
          "title": "Other",
          "next_node": "Talk to Jack",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          }
        }
      ]
    },
    "Work Related Injury": {
      "input": "display",
      "options": [
        {
          "title": "Talk to Jack",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "none"
        }
      ]
    },
    "You are only entitled for ADA: Is it a Disability?": {
      "input": "button",
      "options": [
        {
          "title": "Yes",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Talk to Jack"
        },
        {
          "title": "No",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Your reason does not qualify for protected leave"
        }
      ]
    },
    "Serious Health Condition Family": {
      "input": "button",
      "options": [
        {
          "title": "explanation of Serious Health Condition Family (Place holder)",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "none"
        },
        {
          "title": "Continue",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Which Family member is suffering a serious health condition?"
        }
      ]
    },
    "Serious Health Condition Self": {
      "input": "button",
      "options": [
        {
          "title": "Employee’s own serious health condition. Includes disability related to pregnancy* or childbirth. *May be entitled to additional leave if for pregnancy related reasons. See OFLA Pregnancy Disability.",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Description of serious health condition"
        },
        {
          "title": "Continue",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "List of SERIOUS HEALTH CONDITIONS"
        }
      ]
    },
    "Description of serious health condition": {
      "input": "display",
      "options": [
        {
          "title": "A serious health condition is an illness, injury, impairment, or physical or mental condition that incapacitates you or an eligible family member for 3 consecutive days or longer, and involves at least one of the following: Hospital care, Absence plus treatment, Pregnancy, Chronic conditions, Permanent/Long-term conditions requiring supervision, Multiple treatments (Non-chronic conditions), Important definitions for understanding what qualifies as a serious health conditions include: ,Incapacity: the inability to work, attend school or perform other regular daily activities due to a serious health condition or treatment for or recovery from a serious health condition , Treatment: includes examinations to determine if a serious health condition exists and evaluations of the condition. It does not include routine physical examinations, eye examinations or dental examinations",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Description of serious health condition"
        }
      ]
    },
    "List of SERIOUS HEALTH CONDITIONS": {
      "input": "drop down",
      "options": [
        {
          "title": "Hospital care:  Inpatient care (i.e., an overnight stay) in a hospital, hospice, or residential medical care facility, including any period of incapacity or subsequent treatment in connection with or as a consequence of inpatient care.",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Description of serious health condition"
        },
        {
          "title": "Absence plus treatment:  A period of incapacity of more than three consecutive calendar days, including any subsequent treatment or period of incapacity relating to the same condition, that also involves: Two or more treatments by a health care provider, nurse or physician's assistant under the direct supervision of a health care provider, or by a provider of health care services (e.g., physical therapist) under the orders of, or on referral by, a health care provider; or One treatment by a health care provider which results in a regimen of continuing treatment under the supervision of a healthcare provider.",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "List of SERIOUS HEALTH CONDITIONS"
        },
        {
          "title": "Pregnancy: Any period of incapacity for pregnancy-related disabilities or illnesses, or for prenatal care..",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "List of SERIOUS HEALTH CONDITIONS"
        },
        {
          "title": "Chronic conditions: A chronic condition exists when the condition: Requires at least 2 visits a year for treatment by health care provider or by a nurse or physician's assistant under the direct supervision of a health care provider; Continues over an extended period of time (including recurring episodes of a single underlying condition); andMay cause episodic rather than a continuing period of incapacity (e.g., asthma, diabetes, epilepsy).",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "List of SERIOUS HEALTH CONDITIONS"
        },
        {
          "title": "Permanent/Long-term conditions requiring supervision: A period of incapacity that is permanent or long-term due to a condition for which treatment is potentially ineffective. The employee or family member is under the supervision of a health care provider, not necessarily receiving active treatment. Examples include Alzheimer's disease, a severe stroke, or the terminal stages of a disease",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "List of SERIOUS HEALTH CONDITIONS"
        },
        {
          "title": "Multiple treatments (Non-chronic conditions): Any period of absence to receive multiple treatments (including any period of recovery time) by a health care provider or by a provider of health care services under the orders of, or on referral by, a health care provider, either for restorative surgery after an accident or other injury, or for a condition that would likely result in a period of incapacity of more than three consecutive calendar days in the absence of medical intervention or treatment, such as cancer (chemotherapy, radiation, etc.), severe arthritis (physical therapy), and kidney disease (dialysis). ",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "List of SERIOUS HEALTH CONDITIONS"
        }
      ]
    },
    "Talk to Jack": {
      "input": "Display",
      "options": [
        {
          "title": "Hospital care:  Inpatient care (i.e., an overnight stay) in a hospital, hospice, or residential medical care facility, including any period of incapacity or subsequent treatment in connection with or as a consequence of inpatient care.",
          "add_hours": {
            "hours": 0,
            "type": "n/a"
          },
          "next_node": "Description of serious health condition"
        }
      ]
    }
  }

  }),
  computed: {
    
  },
  components: {
    BtnQuestion,
  },
  methods: {
    optionSelected(selected) {
      console.log(selected)
      //do any relevant stuff here
      this.currentNode = this.Nodes[this.currentNode].options[selected].next_node;
    }
  }
}



</script>
<!-- styling for the component -->
<style>
#questions {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>