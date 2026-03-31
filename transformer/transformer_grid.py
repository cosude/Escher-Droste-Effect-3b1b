import numpy as np

def Original_function(out_width, out_height, center_x, center_y,
                        inner_width, zoom_factor=4.0):

    y, x = np.indices((out_height, out_width), dtype=np.float64)

    X = x - center_x
    Y = y - center_y

    Z = X + 1j * Y
    Z[Z == 0] = 1e-8 + 1e-8j

    alpha = np.log(zoom_factor) / (2 * np.pi)
    P = 1 + 1j * alpha
    Z_src = Z ** P

    M = np.maximum(np.abs(Z_src.real), np.abs(Z_src.imag))
    M = np.where(M == 0, 1e-8, M)

    R_min = inner_width / 2.0
    log_base = np.log(zoom_factor)

    k = np.floor(np.log(M / R_min) / log_base)
    scale = zoom_factor ** (-k)

    Z_wrapped = Z_src * scale

    map_x = Z_wrapped.real + center_x
    map_y = Z_wrapped.imag + center_y
    map_x = np.flip(map_x, axis=(0, 1))
    map_y = np.flip(map_y, axis=(0, 1))

    return map_x.astype(np.float32), map_y.astype(np.float32)

def _complex_to_flipped_maps(Z, center_x, center_y):
    map_x = Z.real + center_x
    map_y = Z.imag + center_y
    map_x = np.flip(map_x, axis=(0, 1))
    map_y = np.flip(map_y, axis=(0, 1))
    return map_x.astype(np.float32), map_y.astype(np.float32)

def prepare_droste_data(out_width, out_height, center_x, center_y, inner_width, zoom_factor, log_view_tiles=3.14):
    y, x = np.indices((out_height, out_width), dtype=np.float64)
    Z = (x - center_x) + 1j * (y - center_y)
    Z[Z == 0] = 1e-8 + 1e-8j
    
    alpha = np.log(zoom_factor) / (2 * np.pi)
    P = 1 + 1j * alpha 
    ln_r_period = np.log(zoom_factor)
    R_min = inner_width / 2.0
    
    ln_r_start = np.log(R_min) - (log_view_tiles - 1.0) * (ln_r_period / 2.0)
    theta_start = -np.pi * log_view_tiles
    
    grid_ln_r = (x / out_width) * (ln_r_period * log_view_tiles) + ln_r_start
    grid_theta = (y / out_height) * (2 * np.pi * log_view_tiles) + theta_start 
    
    W_log = grid_ln_r + 1j * grid_theta
    map1 = ((np.exp(W_log).real + center_x).astype(np.float32), 
            (np.exp(W_log).imag + center_y).astype(np.float32))

    Z_slanted = np.exp(W_log * P)
    map2 = ((Z_slanted.real + center_x).astype(np.float32), 
            (Z_slanted.imag + center_y).astype(np.float32))

    Z_src = Z ** P
    
    def zoom_provider(t, zoom_in=True):
        """Generates the seamless Droste zooming map for a given progression t (0.0 to 1.0)."""
        direction = 1 if zoom_in else -1
        
        Z_scaled = Z_src * (zoom_factor ** (-t * direction))
        
        M_scaled = np.maximum(np.abs(Z_scaled.real), np.abs(Z_scaled.imag))
        M_scaled = np.where(M_scaled == 0, 1e-8, M_scaled)
        
        k_dynamic = np.floor(np.log(M_scaled / R_min) / ln_r_period)
        
        Z_final = Z_scaled * (zoom_factor ** -k_dynamic)

        return _complex_to_flipped_maps(Z_final, center_x, center_y)

    return map1, map2, zoom_provider