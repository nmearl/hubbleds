from datetime import datetime

import astropy.units as u
import ipyvue as v
from astropy.coordinates import Angle
from cosmicds.utils import RepeatedTimer, load_template
from ipywidgets import DOMWidget, widget_serialization
# from pywwt.jupyter import WWTJupyterWidget
from ipywwt import WWTWidget
from traitlets import Bool, Instance, Int


class ExplorationTool(v.VueTemplate):
    template = load_template("exploration_tool.vue", __file__,
                             traitlet=True).tag(sync=True)
    widget = Instance(DOMWidget, allow_none=True).tag(sync=True,
                                                      **widget_serialization)
    pan_count = Int(0).tag(sync=True)
    zoom_count = Int(0).tag(sync=True)
    exploration_complete = Bool(False).tag(sync=True)
    dialog = Bool(False).tag(sync=True)
    _fov = Angle(0 * u.deg)
    _ra = Angle(0 * u.deg)
    _dec = Angle(0 * u.deg)
    _panning = False
    _zooming = False

    PANS_NEEDED = 1
    ZOOMS_NEEDED = 1
    UPDATE_TIME = 1  # seconds

    def __init__(self, *args, **kwargs):
        # self.widget = WWTJupyterWidget(hide_all_chrome=True)
        self.widget = WWTWidget()
        self.widget.foreground = 'Digitized Sky Survey (Color)'
        self.widget.background = 'Digitized Sky Survey (Color)'
        self.widget._set_message_type_callback('wwt_view_state',
                                               self._handle_view_message)
        self.last_update = datetime.now()
        self._rt = RepeatedTimer(self.UPDATE_TIME, self._update_if_needed)
        super().__init__(*args, **kwargs)

    def _update_if_needed(self):
        delta = datetime.now() - self.last_update
        if delta.total_seconds() >= self.UPDATE_TIME:
            self._update_zooming(False)
            self._update_panning(False)
            self._check_if_complete()

    def _update_zooming(self, zooming):
        if not zooming and self._zooming:
           #print("Updating zoom count")
            self.zoom_count += 1
        self._zooming = zooming

    def _update_panning(self, panning):
        if not panning and self._panning:
            self.pan_count += 1
        self._panning = panning

    def _check_if_complete(self):
        if self.pan_count >= self.PANS_NEEDED or self.zoom_count >= self.ZOOMS_NEEDED:
            self.exploration_complete = True
            self.widget._set_message_type_callback('wwt_view_state', None)
            self._rt.stop()

    def _handle_view_message(self, wwt, _updated):
        fov = Angle(wwt.get_fov())
        center = wwt.get_center()
        ra = Angle(center.ra)
        dec = Angle(center.dec)
        zooming = not u.isclose(fov, self._fov)
        panning = not u.allclose([ra, dec], [self._ra, self._dec])
        self._update_panning(panning)
        self._update_zooming(zooming)
        self._ra = ra
        self._dec = dec
        self._fov = fov
        self.last_update = datetime.now()
        self._check_if_complete()
