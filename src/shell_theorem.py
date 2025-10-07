import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16}) # 전역 폰트 크기 설정

# ── 물리 상수 및 매개변수 ─────────────────────────────────
G   = 6.67430e-11      # 중력 상수 [m^3 kg^-1 s^-2]
rho = 5510            # 밀도 예시 [kg/m^3]
a   = 6.4e6           # 외부 반지름 a [m]
b   = 3.5e6           # 내부 빈 공간 반지름 b [m]

# 속이 빈 구의 전체 질량 M
M = 4 * np.pi * rho * (a**3 - b**3) / 3

# R 값 범위: 0에서 2a까지 (R=0 부근은 0이 아닌 작은 값으로 대체)
R = np.linspace(1e-3, 2*a, 1000)

# ── 퍼텐셜 Φ(R) 계산 ─────────────────────────────────────
Phi = np.empty_like(R)
# 1) 구 외부 (R >= a)
mask_outer = (R >= a)
Phi[mask_outer] = - G * M / R[mask_outer]

# 2) 빈 공간 내부 (R < b): 퍼텐셜은 상수
mask_inner = (R < b)
Phi[mask_inner] = - 2 * np.pi * rho * G * (a**2 - b**2)

# 3) 쉘 내부 (b <= R < a)
mask_shell = (~mask_outer) & (~mask_inner)
Phi[mask_shell] = -4 * np.pi * rho * G * (
    a**2 / 2
    - b**3 / (3 * R[mask_shell])
    - R[mask_shell]**2 / 6
)

# ── 중력장 크기 |g(R)| 계산 ───────────────────────────────
g = np.empty_like(R)
# 1) 구 외부: g = GM/R^2
g[mask_outer] = G * M / R[mask_outer]**2

# 2) 빈 공간 내부: g = 0
g[mask_inner] = 0.0

# 3) 쉘 내부: g = (4πρG/3)*(R - b^3/R^2)
g[mask_shell] = (4 * np.pi * rho * G / 3) * (
    R[mask_shell] - b**3 / R[mask_shell]**2
)

# ── 그래프 그리기 ─────────────────────────────────────────
plt.figure(figsize=(12,8))
plt.plot(R, Phi, label='Φ(R)')
plt.xlabel('Radial distance R', labelpad=30, fontsize=20)
plt.ylabel('Gravitational potential Φ', fontsize=20)
ax = plt.gca()
ax.set_xticks([])                                   # x축 눈금 숫자 제거
ax.set_yticks([])                                   # y축 눈금 숫자 제거
ax.axvline(x=a, color='k', linestyle='--')          # R = a 점선
ax.axvline(x=b, color='k', linestyle='--')          # R = b 점선
ylim = ax.get_ylim()
ax.text(a, ylim[0], 'a', ha='center', va='top', fontsize=18)
ax.text(b, ylim[0], 'b', ha='center', va='top', fontsize=18)
plt.title('Gravitational Potential as a Function of R', fontsize=24)
plt.grid(True)
plt.legend(fontsize=18)

plt.figure(figsize=(12,8))
plt.plot(R, g, label='|g(R)|', color='C1')
plt.xlabel('Radial distance R', labelpad=30, fontsize=20)
plt.ylabel('Magnitude of the field vector |g|', fontsize=20)
ax = plt.gca()
ax.set_xticks([])                                   # x축 눈금 숫자 제거
ax.set_yticks([])                                   # y축 눈금 숫자 제거
ax.axvline(x=a, color='k', linestyle='--')          # R = a 점선
ax.axvline(x=b, color='k', linestyle='--')          # R = b 점선
ylim = ax.get_ylim()
ax.text(a, ylim[0], 'a', ha='center', va='top', fontsize=18)
ax.text(b, ylim[0], 'b', ha='center', va='top', fontsize=18)
plt.title('Magnitude of the Field Vector as a Function of R', fontsize=24)
plt.grid(True)
plt.legend(fontsize=18)

plt.show()