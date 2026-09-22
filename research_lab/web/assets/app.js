'use strict';
(() => {
const $ = id => document.getElementById(id);
const data = window.RESEARCH_LAB_DATA || {demos:[],benchmark:{summary:[]}};
let lang='ko', local=false, running=false, current=null, position=0, timer=null, activeTab='trace';
try { lang=localStorage.getItem('research-lab-language')==='en'?'en':'ko'; } catch (_) {}
const T={
 title:['관측·가정·개입을 분리하는 폐루프','Separate observation, assumptions and intervention'],
 intro:['정답을 보지 않는 수집 정책, 독립 점검 관측, 사후 평가. 실제 생물 데이터 없이 연구 가설의 실패 경계부터 확인합니다.','Truth-blind acquisition, independent audit observations, and post-run evaluation. Probe research failure boundaries without biological datasets.'],
 eyebrow:['OBSERVATION / ASSUMPTION / INTERVENTION','OBSERVATION / ASSUMPTION / INTERVENTION'],synthetic:['SYNTHETIC ONLY','SYNTHETIC ONLY'],biozero:['실제 생물학적 표본 0개','0 real biological units'],
 setup:['실험 구성','Experiment settings'],scenario:['시나리오','Scenario'],policy:['수집 정책','Acquisition policy'],seed:['시드','Seed'],budget:['예산 상한','Budget ceiling'],observer:['관측 가정','Observation assumption'],run:['새 합성 실험 실행','Run synthetic experiment'],copy:['복사','Copy'],import:['실행 기록 열기','Import execution record'],export:['현재 기록 저장','Export current record'],
 'setup-note':['GitHub Pages에서는 저장된 기록을 검토합니다. Python 서버로 열면 이 화면에서 새 실험을 실행할 수 있습니다.','GitHub Pages reviews stored records. Start the local Python server to execute new experiments from this interface.'],docs:['구현 범위·실행 문서 ↗','Implementation and setup ↗'],runrecord:['ACTUAL EXECUTION RECORD','ACTUAL EXECUTION RECORD'],trace:['폐루프 기록','Loop trace'],prediction:['사후 예측 평가','Post-run evaluation'],benchmark:['반복 실험 비교','Repeated experiments'],scope:['가정·연구 범위','Assumptions and scope'],
 timeline:['수집·점검 타임라인','Acquisition and audit timeline'],replayhint:['재생은 완료된 실행 기록을 이동합니다. 새로운 계산이 아닙니다.','Playback steps through a completed trace. It does not perform a new computation.'],play:['재생','Play'],pause:['일시정지','Pause'],belief:['후보 가정의 상대 비중','Relative candidate belief'],beliefhint:['후보 집합 안에서의 posterior입니다. 높은 값이 실제 기전의 검증을 뜻하지 않습니다.','Posterior weights are conditional on the candidate set. High confidence is not mechanism validation.'],decision:['선택 근거와 비교 후보','Decision evidence and alternatives'],
 'evaluation-note':['수집을 모두 마친 뒤에만 계산한 결과입니다. 이 값과 시뮬레이터 정답은 수집 정책에 전달되지 않습니다.','Computed only after acquisition finishes. These values and simulator truth are never passed to the policy.'],
 finalprediction:['최종 단계의 미관측 조건 예측','Final prediction at held-out conditions'],intervalnote:['점별 95% 관측 예측구간. 동시 구간이나 생물학적 신뢰구간이 아닙니다.','Pointwise 95% observation-predictive intervals. Not simultaneous or biological-population intervals.'],learningcurve:['비용 대비 예측 오차','Prediction error against acquired cost'],ablations:['모듈 제거·관측 가정 변경 비교 포함','Include removal and observer ablations'],benchcaveat:['같은 예산 상한을 적용했지만 실제 지출은 정책마다 다를 수 있습니다. 경고 장치의 구간 확대는 높은 coverage와 낮은 정확도를 동시에 만들 수 있습니다.','The budget ceiling is shared; actual spending may differ. Wider fallback intervals can increase coverage without improving accuracy.'],assumptions:['현재 실행의 가정 등록부','Assumption register for this run'],footer:['연구 계획 1.0.0은 보존됩니다. 본 구현은 H1·H2의 제한된 합성 검증이며, 생물학적·임상적 성능을 주장하지 않습니다.','Research plan 1.0.0 is preserved. This implementation is a limited synthetic H1/H2 probe, not biological or clinical evidence.'],readme:['연구 추가 자료','Research extension guide']};
const scenarios={identifiable:['개입으로 구분 가능','Intervention-identifiable'],observational_equivalence:['관측만으로 구분 불가능','Observational equivalence'],hidden_mechanism:['정답이 후보 집합 밖','Truth outside candidates'],sensor_shift:['관측 센서의 가정 불일치','Sensor misspecification'],noise_shift:['잡음 수준의 가정 불일치','Noise misspecification']};
const scenarioHelp={identifiable:['알려진 두 ODE 후보 중 하나가 정답입니다. 개입·측정 채널을 고를 수 있습니다.','One of two known ODE candidates is true. Interventions and readouts are available.'],observational_equivalence:['개입 없이 혼합 신호만 관측합니다. 두 후보가 같은 관측 분포를 만듭니다.','Only mixed baseline observations are available. Both candidates induce the same distribution.'],hidden_mechanism:['학습기가 모르는 추가 항이 있습니다. 후보 중 하나를 강제로 정답이라 하면 실패입니다.','A hidden additional term lies outside the candidates. A forced candidate assertion is a failure.'],sensor_shift:['시뮬레이터에 입력·시간 의존 센서 편향을 넣습니다. 학습기는 이를 모릅니다.','The simulator adds an input/time-dependent sensor bias unknown to the learner.'],noise_shift:['실제 합성 잡음은 가정한 값의 3배입니다. 경고 장치가 놓칠 수도 있습니다.','Synthetic observation noise is three times its nominal value. The alert may miss this.']};
const policies={random:['무작위','Random'],space_filling:['공간 채우기','Space filling'],max_variance:['최대 잠재분산','Maximum latent variance'],model_information:['모델 정보이득 / 비용','Model information / cost'],guarded_information:['점검·탐색 결합 정보이득','Guarded information'],guarded_no_gate:['점검 대응 제거','Without gate response'],guarded_no_exploration:['정기 탐색 제거','Without scheduled exploration']};
const reasonLabels={shared_initial_design:['공통 초기 관측','Shared initial design'],fixed_independent_audit:['고정된 독립 점검','Fixed independent audit'],audit_alert_gp_exploration:['점검 경고 후 GP 탐색','GP exploration after audit alert'],scheduled_space_filling:['정기 공간 탐색','Scheduled space filling'],model_plus_parameter_information_per_cost:['모델·계수 정보이득 / 비용','Model + parameter information / cost']};
const tr = key => (T[key]||[key,key])[lang==='ko'?0:1];
const tx = (ko,en) => lang==='ko'?ko:en;
const name = (obj,key) => (obj[key]||[key,key])[lang==='ko'?0:1];
const esc = s => String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const f = (x,n=3) => typeof x==='number'&&Number.isFinite(x)?x.toFixed(n):'—';
const pct = x => f(100*x,1)+'%';
function notify(message,error=false){$('notification').textContent=message;$('notification').dataset.error=String(error);}
function stop(){if(timer)clearInterval(timer);timer=null;$('play').textContent=tr('play');}
function setRun(run,sync=true){
 if(!run||run.schema_version!=='research-lab-run-1'||!run.research_only||!Array.isArray(run.history)||!run.history.length||run.history.length>1000||!run.evaluation?.final||!Array.isArray(run.evidence)||!run.evaluation?.prediction_panel||!run.config)throw new Error(tx('지원되는 합성 실행 JSON이 아닙니다.','Not a supported synthetic execution JSON.'));
 if(run.information_budget?.biological_units!==0)throw new Error(tx('실제 생물 데이터는 지원하지 않습니다.','Biological data are not supported.'));
 for(const s of run.history)if(!Number.isFinite(s.value)||!Number.isFinite(s.cumulative_cost)||!s.posterior?.weights||!s.query)throw new Error('Invalid trace contract');
 stop();current=run;position=run.history.length-1;
 if(sync){$('scenario').value=run.config.scenario;$('policy').value=run.config.policy;$('seed').value=run.config.seed;$('budget').value=run.config.budget;$('observer').value=run.config.observer;}
 render();
}
function options(){
 const s=$('scenario').value||'identifiable',p=$('policy').value||'guarded_information';
 $('scenario').innerHTML=Object.keys(scenarios).map(k=>`<option value="${k}">${esc(name(scenarios,k))}</option>`).join('');$('scenario').value=s;
 $('policy').innerHTML=Object.keys(policies).map(k=>`<option value="${k}">${esc(name(policies,k))}</option>`).join('');$('policy').value=p;
}
function controls(){
 $('mode').textContent=local?tx('로컬 실행 가능','Local execution enabled'):tx('기록 검토 모드','Recorded review mode');
 $('run').disabled=!local||running;
 for(const id of ['seed','budget','observer'])$(id).disabled=!local||running;
 $('run-help').textContent=local?tx('CPU에서 새로 계산합니다. 외부 API·데이터·가중치를 사용하지 않습니다.','Computes locally on CPU. No external APIs, data, or weights.'):tx('정적 모드에서는 시드 0·예산 24의 저장 기록을 봅니다. 아래 명령으로 새 실험을 활성화합니다.','Static mode contains seed-0, budget-24 records. Use the command below to enable new runs.');
 $('scenario-help').textContent=name(scenarioHelp,$('scenario').value);
}
function metric(label,value,note){return `<div class="metric"><div class="metric-label">${esc(label)}</div><strong>${esc(value)}</strong><span>${esc(note)}</span></div>`;}
function render(){
 controls();if(!current)return;
 const r=current,e=r.evaluation.final;
 $('run-title').textContent=name(scenarios,r.config.scenario)+' / '+name(policies,r.config.policy);
 $('run-id').textContent=r.acquisition_sha256.slice(0,12)+' · seed '+r.config.seed;
 $('metrics').innerHTML=metric(tx('최종 held-out RMSE','Final held-out RMSE'),f(e.id.rmse),tx('신호 단위 · 낮을수록 작음','Signal units · smaller error'))+metric(tx('95% 구간의 관측 포함률','95% interval coverage'),pct(e.id.observation_95_coverage),tx('관측 예측구간 · 명목값 95%','Observation-predictive · nominal 95%'))+metric(tx('평균 예측구간 폭','Mean predictive interval width'),f(e.id.observation_95_width),tx('높은 coverage만으로 판단하지 않음','Assess together with coverage'))+metric(tx('사용한 합성 비용','Synthetic cost spent'),f(r.total_cost,1)+' / '+f(r.config.budget,0),tx('초기·점검 관측 비용 포함','Includes initial and audit observations'));
 let warning='';
 if(r.gate.suspect)warning=tx('점검 경고: 가정과 관측의 불일치가 의심됩니다. GP 전환은 기전 검증이 아니며, 구간이 넓어지거나 예측이 더 나빠질 수 있습니다.','Audit alert: assumed model and observations may disagree. GP fallback is not a validated mechanism; it may widen intervals or worsen predictions.');
 else if(r.config.scenario==='observational_equivalence')warning=tx('식별 한계: 관측만으로 두 후보를 구분할 수 없습니다. 예측 오차가 낮아도 기전 선택은 보류됩니다.','Identifiability limit: the available observations cannot separate the candidates. Low prediction error does not justify mechanism selection.');
 else if(e.id.observation_95_coverage<.8)warning=tx('사후 평가에서 낮은 포함률을 확인했습니다. 점검 경고가 없다는 사실은 가정이 맞다는 증거가 아닙니다.','Post-run evaluation shows undercoverage. Absence of an audit alert does not establish correct assumptions.');
 $('warning').hidden=!warning;$('warning').textContent=warning;
 $('step').max=r.history.length-1;$('step').value=position;
 renderTrace();renderPrediction();renderBenchmark();renderScope();
}
function renderTrace(){
 if(!current)return;const r=current,s=r.history[position],q=s.query,record=r.evidence.find(e=>e.observation.record_id===s.observation_id);
 $('step-label').textContent=`${tx('단계','Step')} ${position+1}/${r.history.length} · ${tx('비용','Cost')} ${f(s.cumulative_cost,1)}`;
 $('previous').disabled=position===0;$('next').disabled=position===r.history.length-1;
 const w=s.posterior.weights,phase=s.phase==='audit'?tx('독립 점검 · 적합 제외','Audit · excluded from fitting'):tx('학습 관측','Training observation');
 $('layers').innerHTML=`<article class="layer"><div><div class="layer-name">OBSERVATION</div><h3>${esc(tx('기록된 관측','Recorded observation'))}</h3><div class="big">${f(s.value,4)}</div><span class="badge">simulated · arbitrary_signal</span></div><dl><dt>${esc(tx('증거 역할','Evidence role'))}</dt><dd>${esc(phase)}</dd><dt>${esc(tx('학습에 사용한 측정 수','Measurements used for fit'))}</dt><dd>${s.fit_n}</dd><dt>${esc(tx('원본 계보 해시','Evidence chain hash'))}</dt><dd>${esc(record?.hash.slice(0,16))}</dd></dl></article>`+
 `<article class="layer"><div><div class="layer-name">ASSUMPTION</div><h3>${esc(tx('후보 가정','Candidate assumptions'))}</h3><span class="badge">${esc(r.config.observer)}</span></div><div><div class="weight-row"><span>Parallel</span><strong>${pct(w.parallel)}</strong></div><div class="bar"><i style="width:${100*w.parallel}%"></i></div><div class="weight-row"><span>Compensatory</span><strong>${pct(w.compensatory)}</strong></div><div class="bar second"><i style="width:${100*w.compensatory}%"></i></div><p class="hint">${esc(s.fallback_active?tx('경고 대응: 예측 GP 사용','Alert response: predictive GP'):s.candidate_preference?tx('합성 후보 선호만 기록','Synthetic candidate preference only'):tx('후보 선택 보류','Candidate selection withheld'))}</p></div></article>`+
 `<article class="layer"><div><div class="layer-name">INTERVENTION / DESIGN</div><h3>${esc(tx('선택한 실험','Selected experiment'))}</h3><span class="badge">${esc(tx('합성 허용 목록 승인','Synthetic allowlist only'))}</span></div><dl><dt>${esc(tx('조건 · 시점 · 개입','Condition · time · intervention'))}</dt><dd>x=${f(q.condition,1)} · t=${f(q.time,1)} · u=${f(q.intervention,0)}</dd><dt>${esc(tx('측정 채널','Readout'))}</dt><dd>${esc(q.readout)}</dd><dt>${esc(tx('선택 근거','Selection reason'))}</dt><dd>${esc(name(reasonLabels,s.selection.reason)===s.selection.reason?name(policies,s.selection.reason):name(reasonLabels,s.selection.reason))}</dd></dl></article>`;
 const xs=r.history.map(h=>h.cumulative_cost),ys1=r.history.map(h=>h.posterior.weights.parallel),ys2=r.history.map(h=>h.posterior.weights.compensatory);
 chart('belief-chart',xs,[{y:ys1,label:'Parallel',color:'#76d8c3'},{y:ys2,label:'Compensatory',color:'#eeb68c'}],{yMin:0,yMax:1,xLabel:tx('수집 비용','Acquisition cost'),vline:s.cumulative_cost});
 $('decision-json').textContent=JSON.stringify({selection:s.selection,approval:s.approval,diagnostic:s.diagnostic,audit:s.audit},null,2);
}
function chart(id,xs,series,opt={}){
 const node=$(id);if(!xs.length){node.textContent='No data';return;}
 const W=Math.max(290,Math.min(810,(document.querySelector('.results')?.clientWidth||842)-32)),H=240,L=52,R=18,T=16,B=40;
 let all=series.flatMap(s=>s.y).filter(Number.isFinite);if(opt.band)all.push(...opt.band.lo,...opt.band.hi);
 let min=opt.yMin??Math.min(...all),max=opt.yMax??Math.max(...all);if(max===min)max=min+1;
 if(opt.yMin===undefined){let pad=(max-min)*.1;min-=pad;max+=pad;}
 let xmin=Math.min(...xs),xmax=Math.max(...xs);if(xmin===xmax)xmax=xmin+1;
 const X=x=>L+(x-xmin)/(xmax-xmin)*(W-L-R),Y=y=>T+(max-y)/(max-min)*(H-T-B);
 let svg=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(opt.aria||series.map(s=>s.label).join(', '))}">`;
 for(let i=0;i<4;i++){let v=min+(max-min)*i/3,y=Y(v);svg+=`<line class="grid" x1="${L}" x2="${W-R}" y1="${y}" y2="${y}"/><text class="axis" x="${L-9}" y="${y+4}" text-anchor="end">${f(v,2)}</text>`;}
 for(let i=0;i<5;i++){let v=xmin+(xmax-xmin)*i/4,x=X(v);svg+=`<text class="axis" x="${x}" y="${H-20}" text-anchor="middle">${f(v,1)}</text>`;}
 if(opt.band){const a=xs.map((x,i)=>`${X(x)},${Y(opt.band.hi[i])}`),b=xs.map((x,i)=>`${X(x)},${Y(opt.band.lo[i])}`).reverse();svg+=`<polygon points="${a.concat(b).join(' ')}" fill="#76d8c3" fill-opacity=".16"/>`;}
 for(const s of series){const points=xs.map((x,i)=>`${X(x)},${Y(s.y[i])}`).join(' ');if(!s.dotsOnly)svg+=`<polyline points="${points}" fill="none" stroke="${s.color}" stroke-width="2.4" ${s.dashed?'stroke-dasharray="5 5"':''}/>`;
 if(s.points||s.dotsOnly)xs.forEach((x,i)=>{svg+=`<circle cx="${X(x)}" cy="${Y(s.y[i])}" r="3.4" fill="${s.color}"/>`;});}
 if(opt.vline!==undefined)svg+=`<line x1="${X(opt.vline)}" x2="${X(opt.vline)}" y1="${T}" y2="${H-B}" stroke="#dae5ed" stroke-dasharray="4 4" opacity=".65"/>`;
 svg+=`<text class="axis" x="${W-R}" y="${H-2}" text-anchor="end">${esc(opt.xLabel||'')}</text></svg>`;
 svg+=`<div class="legend">${series.map(s=>`<span style="--c:${s.color}">${esc(s.label)}</span>`).join('')}${opt.band?`<span style="--c:#76d8c3">${esc(tx('95% 예측구간','95% predictive interval'))}</span>`:''}</div>`;node.innerHTML=svg;
}
function renderPrediction(){
 if(!current)return;const p=current.evaluation.prediction_panel;
 const keys=[...new Set(p.queries.map(q=>`${q.condition}|${q.readout}|${q.intervention}`))];const previous=$('slice').value;
 $('slice').innerHTML=keys.map(k=>{const [x,r,u]=k.split('|');return `<option value="${esc(k)}">x=${x} · ${esc(r)} · u=${u}</option>`;}).join('');
 $('slice').value=keys.includes(previous)?previous:keys.find(k=>k.endsWith('pathway_b|1'))||keys[0];renderSlice();
 const c=current.evaluation.curves;chart('learning-chart',c.map(e=>e.cost),[{y:c.map(e=>e.id.rmse),label:tx('도메인 내','In-domain'),color:'#76d8c3'},{y:c.map(e=>e.ood.rmse),label:tx('외삽 조건','Extrapolation'),color:'#eeb68c'}],{yMin:0,xLabel:tx('비용 (초기·점검 포함)','Cost (including audits)')});
 const e=current.evaluation.final,truth=current.evaluation.truth;
 $('eval-extra').innerHTML=metric(tx('평가용 시뮬레이터 정답','Evaluation-only simulator truth'),truth.candidate_truth,tx('정책에는 비공개','Not exposed to the policy'))+metric(tx('외삽 RMSE','Extrapolation RMSE'),f(e.ood.rmse),tx('학습 범위 밖 조건에서 평가','Conditions outside acquisition range'))+metric(tx('최종 판단','Final decision'),e.abstained?tx('보류','Abstain'):tx('합성 후보 선호','Synthetic preference'),tx('검증된 생물 기전 아님','Not a validated biological mechanism'));
}
function renderSlice(){
 if(!current)return;const p=current.evaluation.prediction_panel,k=$('slice').value;
 const idx=p.queries.map((q,i)=>[q,i]).filter(([q])=>`${q.condition}|${q.readout}|${q.intervention}`===k).map(([,i])=>i).sort((a,b)=>p.queries[a].time-p.queries[b].time);
 chart('prediction-chart',idx.map(i=>p.queries[i].time),[{y:idx.map(i=>p.truth[i]),label:tx('평가용 무잡음 정답','Evaluation-only clean truth'),color:'#eeb68c',dashed:true},{y:idx.map(i=>p.mean[i]),label:tx('최종 예측 평균','Final predictive mean'),color:'#76d8c3',points:true},{y:idx.map(i=>p.noisy_test[i]),label:tx('독립 테스트 관측','Independent test observations'),color:'#d9e3ed',dotsOnly:true}],{band:{lo:idx.map(i=>p.lower[i]),hi:idx.map(i=>p.upper[i])},xLabel:tx('합성 시간','Synthetic time')});
}
function renderBenchmark(){
 const b=data.benchmark||{},s=current?.config.scenario||$('scenario').value;
 $('benchmark-note').textContent=tx(`${b.runs||0}회 실행 · 셀당 ${b.seeds?.length||0}개 독립 합성 세계. 현재 표: ${name(scenarios,s)}. 합성 세계 시드는 생물학적 개체가 아닙니다.`,`${b.runs||0} executions · ${b.seeds?.length||0} independent synthetic worlds per cell. Scenario: ${name(scenarios,s)}. World seeds are not biological units.`);
 $('benchmark-head').innerHTML=[tx('정책 / 관측 가정','Policy / observer'),'RMSE',tx('포함률','Coverage'),tx('구간 폭','Width'),tx('경고율','Alert rate'),tx('보류율','Abstention'),tx('지출','Cost')].map(h=>`<th scope="col">${esc(h)}</th>`).join('');
 const rows=(b.summary||[]).filter(r=>r.scenario===s&&($('ablations').checked||r.track==='main'));
 $('benchmark-body').innerHTML=rows.map(r=>`<tr><td>${esc(name(policies,r.policy))}${r.observer==='identity'?'<br><span class="hint">Identity observer</span>':''}</td><td>${f(r.id_rmse)}</td><td>${pct(r.observation_95_coverage)}</td><td>${f(r.observation_95_width)}</td><td>${pct(r.alert_rate)}</td><td>${pct(r.abstention_rate)}</td><td>${f(r.cost,1)}</td></tr>`).join('');
 const d=b.paired_comparisons?.find(x=>x.scenario===s&&x.policy==='guarded_information'&&x.metric==='rmse');
 $('paired-note').textContent=d?tx(`점검 결합 정책 - 무작위의 시드별 RMSE 차이: ${f(d.mean_paired_difference,4)}. 합성 세계 bootstrap 95% 구간 [${d.bootstrap_95_percentile_interval.map(v=>f(v,4)).join(', ')}]. 생물학적 효과의 신뢰구간이나 다중비교 보정 결과가 아닙니다.`,`Seed-paired RMSE difference, guarded minus random: ${f(d.mean_paired_difference,4)}. Synthetic-world bootstrap 95% interval [${d.bootstrap_95_percentile_interval.map(v=>f(v,4)).join(', ')}]. Not a biological-effect interval or multiplicity-adjusted result.`):tx('이 설정의 반복 비교는 포함되지 않았습니다.','No repeated comparison is included for this setting.');
}
function renderScope(){
 const sections=lang==='ko'?[
 ['실제로 구현한 것','원본 스키마와 연결된 추가 전용 관측 기록, 해시 계보, 두 알려진 ODE 후보의 베이지안 계수 추정, 비용 인지 정보이득, 독립 점검 경고, 예측 GP 전환, 후보 판단 보류, 합성 사후 평가를 실행합니다.'],
 ['구현하지 않은 것','PINN·BINN·SINDy의 학습, 임의 방정식 발견, 바이오 파운데이션 미세조정, 멀티피델리티 획득, 생성 증강, 실제 생명·뇌과학 데이터 연결은 후속 연구 범위입니다. 실제 실험 승인 또는 장치 제어는 없습니다.'],
 ['가정의 범위','두 동역학 후보의 감쇠율과 명목 센서 연산자를 알려진 값으로 둡니다. 계수에는 Gaussian prior를 적용합니다. 관측 교정값을 데이터에서 새로 알아낸 실험이 아닙니다.'],
 ['원본 연구 보존','기존 01~08장과 예제·스키마·근거는 그대로 두었습니다. 09~12장과 research_lab/이 추가 구현·결과·후속 연구 방향을 기록합니다.'],
 ['근거와 차별화','Consensus로 찾은 개입 설계·가정 불일치·식별가능성 연구를 참고했습니다. 이 구현은 CIV, R-IDeA, 최적제어 알고리즘의 재현이나 새로운 정리의 입증이 아닙니다.']
 ]:[
 ['Implemented','An append-only observation ledger compatible with the original schema, hash lineage, Bayesian coefficient fitting for two known ODEs, cost-aware information gain, independent audit alerts, predictive GP fallback, abstention, and offline synthetic evaluation.'],
 ['Not implemented','PINN/BINN/SINDy training, arbitrary equation discovery, biological foundation fine-tuning, multi-fidelity acquisition, generative augmentation, and biological dataset adapters remain future research. No real experiment authorization or device control exists.'],
 ['Assumption boundary','The two candidate decay rates and nominal sensor operator are supplied metadata. Coefficients use Gaussian priors. Sensor calibration is not estimated from data in this experiment.'],
 ['Original research preserved','Chapters 01–08 and their examples, schemas and evidence remain intact. Chapters 09–12 and research_lab/ record the new implementation, findings and research direction.'],
 ['Literature and originality','Consensus-assisted intervention-design, misspecification and identifiability literature informed the design. This is not a reproduction of CIV, R-IDeA or optimal-control algorithms, nor proof of a new theorem.']];
 $('scope-content').innerHTML=sections.map(([h,p])=>`<div class="scope-block"><h3>${esc(h)}</h3><p>${esc(p)}</p></div>`).join('');$('assumption-json').textContent=JSON.stringify(current?.assumptions||{},null,2);
}
function applyLanguage(){$('observer').options[0].textContent=tx('명목 관측 연산자','Nominal sensor operator');$('observer').options[1].textContent=tx('항등 연산자 (비교)','Identity operator (ablation)');document.documentElement.lang=lang;$('language').textContent=lang==='ko'?'EN':'KR';document.querySelectorAll('[data-i]').forEach(el=>el.textContent=tr(el.dataset.i));$('doc-link').href=`../../docs/${lang}/09_EXECUTABLE_RESEARCH.md`;options();render();}
function selectTab(key){activeTab=key;document.querySelectorAll('[role=tab]').forEach(b=>{const yes=b.dataset.tab===key;b.setAttribute('aria-selected',String(yes));b.tabIndex=yes?0:-1;$('panel-'+b.dataset.tab).hidden=!yes;});}
$('language').addEventListener('click',()=>{lang=lang==='ko'?'en':'ko';try{localStorage.setItem('research-lab-language',lang);}catch(_){}applyLanguage();});
for(const id of ['scenario','policy'])$(id).addEventListener('change',()=>{
 controls();if(local)return;
 const r=data.demos.find(d=>d.config.scenario===$('scenario').value&&d.config.policy===$('policy').value);
 if(r){notify('');setRun(r);}else{notify(tx('이 모듈 제거 설정은 반복 결과 표에만 있습니다. 로컬 서버에서 새 기록을 생성하십시오.','This ablation is available in the benchmark table. Run the local server to generate a full trace.'));}
});
$('run').addEventListener('click',async()=>{
 if(!local||running)return;stop();running=true;controls();notify(tx('합성 폐루프를 실행하고 있습니다.','Executing the synthetic loop.'));
 try{const response=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenario:$('scenario').value,policy:$('policy').value,seed:Number($('seed').value),budget:Number($('budget').value),observer:$('observer').value})});const body=await response.json();if(!response.ok)throw new Error(body.error||'Execution failed');setRun(body);notify(tx('새 실행을 완료했습니다. 결과를 JSON으로 저장할 수 있습니다.','New execution complete. Export the result as JSON.'));}
 catch(e){notify(String(e.message),true);}finally{running=false;controls();}
});
$('step').addEventListener('input',()=>{stop();position=Number($('step').value);renderTrace();});
function move(delta){stop();position=Math.max(0,Math.min(current.history.length-1,position+delta));$('step').value=position;renderTrace();}
$('previous').addEventListener('click',()=>move(-1));$('next').addEventListener('click',()=>move(1));
$('play').addEventListener('click',()=>{if(timer){stop();return;}if(position===current.history.length-1)position=0;$('play').textContent=tr('pause');timer=setInterval(()=>{$('step').value=position;renderTrace();if(position>=current.history.length-1){stop();}else position++;},700);});
$('slice').addEventListener('change',renderSlice);$('ablations').addEventListener('change',renderBenchmark);
$('export').addEventListener('click',()=>{const blob=new Blob([JSON.stringify(current,null,2)+'\n'],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`research-${current.config.scenario}-${current.config.policy}-seed${current.config.seed}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
$('import').addEventListener('change',async e=>{try{const file=e.target.files[0];if(!file)return;if(file.size>8*1024*1024)throw new Error(tx('8MB 이하의 실행 JSON만 지원합니다.','Execution JSON must be at most 8 MB.'));setRun(JSON.parse(await file.text()));notify(tx('실행 기록을 불러왔습니다. 재계산하지 않았습니다.','Execution record imported, not recomputed.'));}catch(err){notify(String(err.message),true);}finally{e.target.value='';}});
$('copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText('python -m research_lab serve');notify(tx('실행 명령을 복사했습니다.','Launch command copied.'));}catch(_){notify(tx('명령을 선택해 복사하십시오: python -m research_lab serve','Select and copy: python -m research_lab serve'));}});
const tabs=[...document.querySelectorAll('[role=tab]')];tabs.forEach((b,i)=>{b.addEventListener('click',()=>selectTab(b.dataset.tab));b.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const n=e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;selectTab(tabs[n].dataset.tab);tabs[n].focus();});});
let resizeFrame=null;window.addEventListener('resize',()=>{if(resizeFrame)cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>{if(current){renderTrace();renderPrediction();}});});
applyLanguage();const defaultRun=data.demos.find(d=>d.config.scenario==='identifiable'&&d.config.policy==='guarded_information')||data.demos[0];if(defaultRun)setRun(defaultRun);else notify(tx('포함된 실행 기록을 찾지 못했습니다.','No bundled execution records found.'),true);
if(/^https?:$/.test(location.protocol)&&['127.0.0.1','localhost'].includes(location.hostname))fetch('/api/status').then(r=>r.ok?r.json():null).then(s=>{local=s?.mode==='local-research';controls();}).catch(()=>controls());
})();
