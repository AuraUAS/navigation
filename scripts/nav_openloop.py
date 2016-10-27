import numpy as np
import os
import sys

sys.path.append('../build/src/nav_core/.libs/')
sys.path.append('../build/src/nav_openloop/.libs/')
import libnav_core
import libnav_openloop

class filter():
    def __init__(self):
        self.ekf = libnav_openloop.OpenLoop()
        self.name = 'Open Loop'
        self.filter_sync = 0.0

    def set_state(self, lat, lon, alt, vn, ve, vd, phi, the, psi):
        self.ekf.set_pos(lat, lon, alt)
        self.ekf.set_vel(vn, ve, vd)
        self.ekf.set_att(phi, the, psi)

    def set_pos(self, lat, lon, alt):
        self.ekf.set_pos(lat, lon, alt)

    def set_vel(self, vn, ve, vd):
        self.ekf.set_vel(vn, ve, vd)

    def set_att(self, phi, the, psi):
        self.ekf.set_att(phi, the, psi)
        
    def set_gyro_calib(self, gxb, gyb, gzb, gxs, gys, gzs):
        self.ekf.set_gyro_calib(gxb, gyb, gzb, gxs, gys, gzs)
        
    def set_accel_calib(self, axb, ayb, azb, axs, ays, azs):
        self.ekf.set_accel_calib(axb, ayb, azb, axs, ays, azs)
        
    def init(self, imu, gps, filt):
        self.set_state(filt.lat, filt.lon, filt.alt,
                       filt.vn, filt.ve, filt.vd,
                       filt.phi, filt.the, filt.psi)
        nav = self.ekf.update(imu)
        return nav

    def update(self, imu, gps, filt):
        resync = False
        if resync and filt.time > self.filter_sync + 300:
            print 'resync:', filt.time
            self.filter_sync = filt.time
            nav = self.init(imu, gps, filt)
        else:
            nav = self.ekf.update(imu)
        return nav

    def close(self):
        pass