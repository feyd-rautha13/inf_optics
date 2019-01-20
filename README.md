# Inf optics test code
 ---


#BUS
##socket
##ssh
##telnet





$$ 
y(t) = \int_{-\infty}^{+\infty} x(\tau)h(t-\tau) d\tau{\tag{1.1}}
$$

$$
y[n] = \sum_{k=-\infty}^{+\infty}x[k]h[n-k]{\tag{1.2}}
$$

$$
x(t) = \sum_{k=-\infty}^{\infty}a_ke^{jk\omega_0t}{\tag{1.3}}
$$

$$
x(t) = a_0 + 2\sum_{k=1}^{+\infty}\Re\{a_ke^{jk\omega_0t}\}{\tag{1.4}}
$$

$$
x(t) = a_0 + 2\sum_{k=1}^{+\infty}A_k\cos(k\omega_0t + \theta_k) {\tag{1.5}}
$$

$$
x(t) = a_0 + 2\sum_{k=1}^{+\infty}(B_k\cos{k\omega_0t-C_k\sin{k\omega_0t}}){\tag{1.6}}
$$
$$
a_k=\frac{1}{T}\int_T x(t) e^{-jk\omega_0t}dt{\tag{1.7}}
$$