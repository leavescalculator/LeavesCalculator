<template>
<div style="padding-top: 5px;">
  <button type="button" class="btn btn-info" data-toggle="modal" data-target="#exampleModal">
    Database Logic
  </button>

  <!-- Modal -->
  <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Database Logic</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          “== fmla_eligibility T” —> Eligible for FMLA<br />
          “== ofla_eligibility T” —> Eligible for OFLA<br />
          “== fmla_eligibility F” —>  Not eligible for FMLA<br />
          “== ofla_eligibility F” —> Not eligible for OFLA<br />
          “== ofla_eligibility P” —> Only eligible for Parental OFLA<br />
          “== ofla_eligibility M” —> Only eligible for military OFLA<br />
          “== ofla_eligibility B” —> Eligible for both parental and military OFLA
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  
}
</script>