<template>
  <scaffold-alert
    color="info"
    class="mb-4 mx-auto"
    max-width="800"
    elevation="6"
    title-text="Meet the Spectrum Viewer"
    @back="back_callback()"
    @next="next_callback()"
    :can-advance="can_advance"
  >

    <template #before-next>
      Click <span style="background-color: #02838f; border-radius: 5px; padding: 3px; color:white!important;">SPECTRUM TUTORIAL</span> button.
    </template>

    <div
      class="mb-4"
    >
      <p>
        The <b>spectrum</b> of light measured from the example galaxy is shown in the Spectrum Viewer.
      </p>
      <p>
        (If you scroll up to the Cosmic Sky Viewer, you will see the example galaxy displayed there too.)
      </p>
    </div>
    <div
      v-if="!(state_view.spectrum_tutorial_opened)"
    >    
      <p>
        Click the <span style="background-color: #02838f; border-radius: 5px; padding: 3px; color:white!important;">SPECTRUM TUTORIAL</span> button to learn what spectra can tell us about galaxies.
      </p>
    </div>
    <div
      class="mb-4"
      v-if="state_view.spectrum_tutorial_opened"
    >
      <p>
        You can reopen the <span style="background-color: #02838f; border-radius: 5px; padding: 3px; color:white!important;">SPECTRUM TUTORIAL</span> any time you need a refresher about spectra.
      </p>
    </div>
  </scaffold-alert>
</template>
