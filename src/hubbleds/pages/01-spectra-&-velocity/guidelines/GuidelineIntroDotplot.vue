<template>
  <scaffold-alert
    title-text="Dot plots"
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="can_advance"
  >
    <template #before-next>
      Click <span style="background-color: #02838f; border-radius: 5px; padding: 3px; color:white!important;">DOT PLOT TUTORIAL</span> button.
    </template>

    <div>
      <p>
        This is a <strong>dot plot</strong> of velocity measurements for you and a randomly chosen subset of others who have completed the Hubble Data Story.
      </p>
      <p>
        Your measurement is shown as an orange-red dot.
      </p>
      <p>
        Click the <span style="background-color: #02838f; border-radius: 5px; padding: 3px; color:white!important;">DOT PLOT TUTORIAL</span> button to learn about interpreting dot plots.
      </p>
    </div>
  </scaffold-alert>
</template>
