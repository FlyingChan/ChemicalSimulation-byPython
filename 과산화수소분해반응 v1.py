from chempy import Reaction, Substance
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

# 과산화수소 분해 반응
reaction_equation = '2 H2O2 -> 2 H2O + O2'
reaction = Reaction.from_string(reaction_equation)

# 초기 농도 및 시간 포인트 설정
initial_concentrations = {'H2O2': 1.0, 'H2O': 0.0, 'O2': 0.0}  # 초기 과산화수소 농도 (예: 1 M)
time_span = (0, 10)  # 시간 범위

# 물질 정의
substances = [Substance.from_formula('H2O2'), Substance.from_formula('H2O'), Substance.from_formula('O2')]

# 초기 농도 설정
initial_conditions = [initial_concentrations[species.name] for species in substances]

# 시뮬레이션 함수 정의
def reaction_rate(t, concentrations):
    concentrations_dict = {species.name: conc for species, conc in zip(substances, concentrations)}
    rate_value = reaction.rate(concentrations_dict)
    
    # 반응 속도식이 None을 반환하는 경우에 대한 처리
    if rate_value is None:
        rate_value = 0.0  # 또는 다른 적절한 값으로 설정
    
    return [rate_value]  # 벡터화된 연산을 위해 리스트로 반환

# 시뮬레이션 수행
solution = solve_ivp(reaction_rate, time_span, initial_conditions, t_eval=np.linspace(*time_span, 100), vectorized=True)

# 결과 출력 및 그래프 플로팅
print("Concentrations over time:")
for time, concentrations in zip(solution.t, solution.y.T):
    print(f"Time: {time} s, Concentrations: {concentrations}")

# 그래프 플로팅
plt.plot(solution.t, solution.y[0], label='H2O2')
plt.plot(solution.t, solution.y[1], label='H2O')
plt.plot(solution.t, solution.y[2], label='O2')
plt.xlabel('Time (s)')
plt.ylabel('Concentration (M)')
plt.legend()
plt.show()
