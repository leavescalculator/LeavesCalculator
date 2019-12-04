<template>
<div style="padding-top: 5px;">
  <b-button v-b-modal.modal-1 variant="info">Database Logic</b-button>

  <b-modal ok-only id="modal-1" title="Database Logic">
    <p class="my-4">
      “== fmla_eligibility T” —> Eligible for FMLA<br />
          “== ofla_eligibility T” —> Eligible for OFLA<br />
          “== fmla_eligibility F” —>  Not eligible for FMLA<br />
          “== ofla_eligibility F” —> Not eligible for OFLA<br />
          “== ofla_eligibility P” —> Only eligible for Parental OFLA<br />
          “== ofla_eligibility M” —> Only eligible for military OFLA<br />
          “== ofla_eligibility B” —> Eligible for both parental and military OFLA
    </p>
  </b-modal>
</div>
</template>

<script>
export default {
  
}
</script>