<template>
  <!-- TODO: update when students have measurements 
    <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    :title-text="state.angsizes_total < 5 ? 'Repeat for Remaining Galaxies' : 'Nice Work'"
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="can_advance"
  > -->
  <scaffold-alert
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="can_advance"
  >
    <template #before-next>
      <!-- <span v-if="!state.bad_angsize">
        Measure angular size<span v-if="state.angsizes_total < 4">s</span> for {{ 5 - state.angsizes_total }} more <span v-if="state.angsizes_total < 4">galaxies</span><span v-if="state.angsizes_total == 4">galaxy</span>.
      </span>
      <span v-if="state.bad_angsize">
        <b>Remeasure angular size</b>
        <br/>
      </span> -->
    </template>

    <v-card color="error">
      <v-card-text>
        This guideline needs to be fixed once we wire up student measurements
      </v-card-text>
    </v-card>

    <!-- If there are no bad measurements and measurements are not complete -->
    <!-- <div
      class="mb-4"
      v-if="state.angsizes_total < 5 && !state.bad_angsize"
    >
      <p>
        Repeat the angular size measurements for each of the remaining galaxies in your table.
      </p>
    </div> -->

    <!-- If there are any bad measurements -->
    <!-- <div
      class="mb-4"
      v-if="state.bad_angsize"
    >
      <p>
        Your measured angular size is not within the expected range. Please try again.
      </p>
      <p>
        Ask your instructor if you are not sure where to measure.
      </p>
    </div> -->

    <!-- If measurements are complete and there are no bad measurements -->  
    <!-- <div
      class="mb-4"
      v-if="state.angsizes_total >= 5 && !state.bad_angsize"
    >
      <p>
        You have measured angular sizes for all of your galaxies.
      </p>
      <p>
        You can continue to refine your measurements, or, if you are satisfied, you can move on.
      </p>
    </div> -->
  </scaffold-alert>
</template>
<script>
</script>
