/* No external dependencies; works via file://, GitHub Pages, or the local runner. */
(async () => {
'use strict';
const $ = id => document.getElementById(id);
let bundle;
try { bundle = await window.CLOSED_LOOP_READY; }
catch (error) {
 document.getElementById('status-message').textContent = '데이터를 읽지 못했습니다. 최신 Chrome/Edge/Firefox에서 열고 lab/data/pilot-data.js를 확인하세요. / Cannot load included data. Use a current browser with DecompressionStream support.';
 document.getElementById('status-message').style.display = 'block';
 console.error(error); return;
}
let lang = 'ko'; try { lang = localStorage.getItem('closed-loop-language') === 'en' ? 'en' : 'ko'; } catch (_) {}
let current = null, stepIndex = 0, timer = null, csrfToken = null, busy = false, source = 'bundled';
let messageTimer;
const t = key => window.LAB_I18N[lang][key] || key;
const esc = value => { const node = document.createElement('span'); node.textContent = String(value); return node.innerHTML; };
const fmt = (value, digits = 3) => Number.isFinite(value) ? value.toFixed(digits) : '—';
const percent = value => Number.isFinite(value) ? `${(100 * value).toFixed(1)}%` : '—';
const nameScenario = key => window.LAB_SCENARIOS[key]?.[lang === 'ko' ? 0 : 1] || key;
const namePolicy = key => window.LAB_POLICIES[key]?.[lang === 'ko' ? 0 : 1] || key;
function message(text) { $('status-message').textContent = text; $('status-message').style.display = 'block'; clearTimeout(messageTimer); messageTimer = setTimeout(() => $('status-message').style.display = 'none', 5000); }
function options(select, entries, selected) { select.replaceChildren(); entries.forEach(([value, text]) => { const option = document.createElement('option'); option.value = value; option.textContent = text; select.append(option); }); if (entries.some(e => e[0] === selected)) select.value = selected; }
function policies(scenario) {
 if (scenario.startsWith('fidelity_')) return ['hf_only','naive_pool','multifidelity','guarded'];
 if (['confounded','biased_sensor','missing_term','mechanism_pair','mechanism_outside'].includes(scenario)) return ['random','fixed_readout','observation_variance','information_gain','guarded'];
 return ['random','space_filling','max_variance','guarded'];
}
function updateDesign() {
 const scenario = $('scenario').value, previous = $('policy').value;
 options($('policy'), policies(scenario).map(p => [p, namePolicy(p)]), previous || 'guarded');
 $('scenario-description').textContent = window.LAB_SCENARIOS[scenario][lang === 'ko' ? 2 : 3];
 $('observation-model').disabled = !['confounded','biased_sensor','missing_term'].includes(scenario);
 if ($('observation-model').disabled) $('observation-model').value = 'aware';
}
function labels() {
 document.documentElement.lang = lang;
 document.querySelectorAll('[data-i18n]').forEach(node => node.textContent = t(node.dataset.i18n));
 $('lang-toggle').textContent = lang === 'ko' ? 'EN' : '한국어';
 const locale = lang === 'ko' ? 'ko' : 'en';
 $('docs-link').href = `research/docs/${locale}/09_IMPLEMENTATION.md`;
 $('results-link').href = `research/docs/${locale}/11_PILOT_RESULTS.md`;
 $('roadmap-link').href = `research/docs/${locale}/12_RESEARCH_DIRECTION.md`;
 $('baseline-link').href = lang === 'ko' ? 'README.md' : 'README.en.md';
 const scenario = $('scenario').value || 'confounded', compare = $('comparison-scenario').value || 'confounded';
 const list = Object.keys(window.LAB_SCENARIOS).map(s => [s, nameScenario(s)]);
 options($('scenario'), list, scenario); options($('comparison-scenario'), list, compare);
 const operator = $('observation-model').value;
 options($('observation-model'), [['aware',t('aware')],['identity',t('identity')]], operator);
 updateDesign(); updateMode(); renderAgenda(); renderComparison(); if (current) render();
}
function updateMode() {
 $('mode-label').textContent = t(csrfToken ? 'liveMode' : 'staticMode');
 $('mode-label').classList.toggle('live', !!csrfToken);
 $('run-new').disabled = busy || !csrfToken;
 $('runner-note').textContent = t(csrfToken ? 'liveNote' : 'offlineNote');
}
function validateRun(run) {
 if (!run || run.schema_version !== '1.1.0' || run.evidence_status !== 'synthetic-pilot-only' || run.real_data_validation !== false) return false;
 if (!run.config || !window.LAB_SCENARIOS[run.config.scenario] || !Array.isArray(run.snapshots) || !run.snapshots.length || run.snapshots.length > 500 || !Array.isArray(run.observations) || run.observations.length > 2000 || !Array.isArray(run.events) || run.events.length > 8000 || !run.final || !run.budget || !run.model_card) return false;
 if (!run.observations.every(r => r.origin === 'simulated' && r.counts_as_new_biological_unit === false && r.query && Number.isFinite(r.value))) return false;
 return run.snapshots.every(s => s.predictions && s.assumptions && Object.values(s.predictions).every(p => ['x','mean','lower','upper'].every(key => Array.isArray(p[key]) && p[key].length > 0 && p[key].length <= 4000 && p[key].length === p.x.length && p[key].every(Number.isFinite))));
}
function stopPlay() { if (timer) clearInterval(timer); timer = null; $('play').textContent = t('replay'); }
function setRun(run, kind) {
 if (!validateRun(run)) throw new Error(t('invalidFile'));
 stopPlay(); current = run; source = kind; stepIndex = run.snapshots.length - 1;
 $('scenario').value = run.config.scenario; updateDesign(); $('policy').value = run.config.policy;
 $('observation-model').value = run.config.observation_model; $('seed').value = run.config.seed; $('budget').value = run.config.training_budget;
 $('step-range').max = current.snapshots.length - 1;
 $('comparison-scenario').value = run.config.scenario; renderComparison(); render();
}
function loadBundled() {
 const scenario = $('scenario').value, policy = $('policy').value, operator = $('observation-model').value, seed = Number($('seed').value), budget = Number($('budget').value);
 const record = bundle?.runs.find(r => r.config.scenario === scenario && r.config.policy === policy && r.config.observation_model === operator && r.config.seed === seed && r.config.training_budget === budget);
 if (!record) return message(t('noRecord'));
 setRun(record, 'bundled'); message(t('loaded'));
}
function pairs(node, entries) { node.innerHTML = entries.map(([a,b]) => `<dt>${esc(a)}</dt><dd>${esc(b)}</dd>`).join(''); }
function reasonText(reason) {
 const translations = {
 'projected-information-gain-per-cost':['관측 정보이득 / 비용','Projected information / cost'],
 'hf-integrated-variance-reduction-per-cost':['HF 통합 분산 감소 / 비용','HF integrated variance reduction / cost'],
 'maximum-projected-latent-variance':['관측에 투영한 잠재 분산','Projected latent variance'],
 'farthest-observed-condition':['관측 조건에서 가장 먼 위치','Farthest from observed conditions'],
 'uniform-random-eligible-query':['허용 질의에서 무작위','Random eligible query'],
 'random-exploration':['지정된 탐색 단계','Scheduled random exploration']
 }; return translations[reason]?.[lang === 'ko' ? 0 : 1] || reason;
}
function stopText(reason) {
 const map = {'training-budget-exhausted':['학습 비용 한도 도달','Training cost limit reached'],'no-affordable-eligible-query':['남은 비용으로 가능한 질의 없음','No affordable eligible query'],'max-steps':['단계 한도 도달','Step limit reached'],'assumption-challenged-revise-observation-or-mechanism':['관측·기전 가정 재검토','Revise observation or mechanism assumptions']};
 return map[reason]?.[lang === 'ko' ? 0 : 1] || reason;
}
function render() {
 const snapshot = current.snapshots[stepIndex], final = stepIndex === current.snapshots.length - 1, result = final ? current.final : snapshot.diagnostic;
 $('run-title').textContent = `${nameScenario(current.config.scenario)} · ${namePolicy(current.config.policy)}`;
 $('run-meta').textContent = `seed ${current.config.seed} · ${current.run_id} · ${t('total')} ${fmt(current.budget.total_measurement_cost,2)}`;
 $('run-state').textContent = final ? t(current.stop_reason.startsWith('assumption-challenged') ? 'needsRevision' : 'finalFrozen') : t('inProgress');
 $('run-state').classList.toggle('warn', snapshot.gate.status === 'challenged');
 $('source-status').textContent = t(source === 'live' ? 'sourceLive' : source === 'import' ? 'sourceImport' : 'sourceBundled');
 $('metric-rmse-label').textContent = t(final ? 'finalRMSE' : 'diagnosticRMSE'); $('metric-rmse').textContent = fmt(result.rmse_observed);
 $('metric-rmse-note').textContent = final ? `${t('latentError')} ${fmt(result.rmse_latent)}` : t('diagnosticUse');
 $('metric-coverage-label').textContent = t('coverageLabel'); $('metric-coverage').textContent = percent(result.observation_95_coverage);
 $('metric-width').textContent = `${t('width')} ${fmt(result.observation_95_mean_width)}`;
 $('metric-cost').textContent = `${fmt(snapshot.cost,1)} / ${fmt(current.config.training_budget,0)}`;
 $('metric-n').textContent = `${snapshot.n_train} ${t('measurements')}`;
 $('step-range').value = stepIndex; $('step-label').textContent = `${stepIndex} / ${current.snapshots.length - 1}`;
 $('timeline-note').textContent = t(final ? 'timelineFinal' : 'timelineDuring'); $('chart-note').textContent = t('chartUnit');
 $('show-truth').disabled = !final;
 const readouts = Object.keys(snapshot.predictions);
 options($('chart-readout'), readouts.map(key => [key, t(key === 'first/none' ? 'firstView' : key === 'sum/attenuate_b' ? 'intervenedView' : 'sumView')]), $('chart-readout').value);
 const training = current.observations.filter(r => r.split === 'train').slice(0, snapshot.n_train), last = training[training.length - 1];
 pairs($('observation-detail'), [[t('condition'),fmt(last.query.condition)],[t('readout'),t(last.query.readout)],[t('value'),fmt(last.value)],[t('noise'),fmt(last.noise_sd,2)],[t('replicate'),last.query.replicate],[t('origin'),last.origin],[t('partition'),'train']]);
 const assumptionNames = {'measurement-noise':'assumptionNoise','observation-operator':'assumptionOperator','parameter-separation':'assumptionRank','candidate-library':'assumptionLibrary','kernel-smoothness':'assumptionKernel','fidelity-relation':'assumptionFidelity'};
 const statuses = {'declared-not-estimated':'declared','not-rejected-on-reused-diagnostic':'notRejected','challenged-not-localized':'challenged','not-identified':'rank1','rank-two-under-assumed-operator':'rank2','excluded-after-fallback':'excluded'};
 $('assumption-detail').innerHTML = snapshot.assumptions.map(a => `<div class="assumption-row ${a.status.includes('challenged') || a.status === 'not-identified' ? 'challenged' : ''}">${esc(t(assumptionNames[a.assumption_id] || a.assumption_id))}<span>${esc(t(statuses[a.status] || a.status))}</span></div>`).join('');
 if (snapshot.candidate_probabilities) { const box = document.createElement('div'); box.className = 'assumption-row'; box.textContent = `${t('candidateP')}: ${snapshot.candidate_probabilities.map(p => percent(p)).join(' / ')}`; $('assumption-detail').append(box); }
 const proposal = current.events.find(e => e.type === 'query_proposed' && e.payload.step === snapshot.step + 1);
 if (!final && proposal) { const q = proposal.payload.query; pairs($('intervention-detail'), [[t('condition'),fmt(q.condition)],[t('readout'),t(q.readout)],[t('intervention'),t(q.intervention)],[t('fidelity'),t(q.fidelity)],[t('cost'),fmt(proposal.payload.cost,2)],[t('queryScore'),fmt(proposal.payload.score,5)],[t('reason'),reasonText(proposal.payload.reason)]]); }
 else pairs($('intervention-detail'), [[t('endLoop'),final ? t('finalFrozen') : '—'],[t('stop'),stopText(current.stop_reason)],[t('budgetLeft'),fmt(current.config.training_budget - snapshot.cost,2)]]);
 const decisions = current.events.filter(e => e.type === 'query_proposed' && e.payload.step <= snapshot.step).map(e => e.payload).slice(-12);
 $('decision-rows').innerHTML = decisions.length ? decisions.map(e => `<tr><td class="number">${e.step}</td><td class="number">${fmt(e.query.condition)}</td><td>${esc(t(e.query.readout))}</td><td>${esc(t(e.query.intervention))}</td><td>${esc(t(e.query.fidelity))}</td><td class="number">${fmt(e.cost,2)}</td><td>${esc(reasonText(e.reason))}</td></tr>`).join('') : `<tr><td colspan="7">${esc(t('noDecision'))}</td></tr>`;
 drawChart(snapshot, training, final); $('play').textContent = t(timer ? 'pause' : 'replay');
 $('prev-step').disabled = $('first-step').disabled = stepIndex === 0;
 $('next-step').disabled = $('last-step').disabled = final;
}
function drawChart(snapshot, training, final) {
 const key = $('chart-readout').value, prediction = snapshot.predictions[key], [readout, intervention] = key.split('/');
 const points = training.filter(r => r.query.readout === readout && r.query.intervention === intervention);
 const reference = final && $('show-truth').checked ? current.synthetic_reference_after_freeze?.[key] : null;
 const width = Math.max(300, $('response-chart').clientWidth), height = $('response-chart').clientHeight || 278;
 const left=48, right=14, top=14, bottom=40, chartW=width-left-right, chartH=height-top-bottom;
 const values = [...prediction.lower,...prediction.upper,...points.map(r=>r.value),...(reference?.y || [])];
 let lo=Math.min(...values), hi=Math.max(...values), pad=Math.max((hi-lo)*0.13,0.1); lo-=pad; hi+=pad;
 const x=value=>left+value*chartW, y=value=>top+(hi-value)/(hi-lo)*chartH;
 const path=(xs,ys)=>xs.map((v,i)=>`${i?'L':'M'}${fmt(x(v),2)},${fmt(y(ys[i]),2)}`).join(' ');
 let grid=''; for(let i=0;i<=4;i++){const value=lo+(hi-lo)*i/4;grid+=`<line class="grid" x1="${left}" y1="${y(value)}" x2="${width-right}" y2="${y(value)}"/><text class="axis-label" x="${left-8}" y="${y(value)+4}" text-anchor="end">${fmt(value,1)}</text>`;}
 for(let i=0;i<=4;i++){const value=i/4;grid+=`<text class="axis-label" x="${x(value)}" y="${height-18}" text-anchor="middle">${fmt(value,2)}</text>`;}
 const band=path(prediction.x,prediction.upper)+' '+prediction.x.slice().reverse().map((v,i)=>`L${fmt(x(v),2)},${fmt(y(prediction.lower[prediction.lower.length-1-i]),2)}`).join(' ')+' Z';
 const samples=points.map(r=>r.query.fidelity==='low'?`<rect class="sample-lf" x="${x(r.query.condition)-3.5}" y="${y(r.value)-3.5}" width="7" height="7"><title>${esc(`${t('low')} x=${fmt(r.query.condition)} y=${fmt(r.value)}`)}</title></rect>`:`<circle class="sample" cx="${x(r.query.condition)}" cy="${y(r.value)}" r="4"><title>${esc(`${t('high')} x=${fmt(r.query.condition)} y=${fmt(r.value)}`)}</title></circle>`).join('');
 $('response-chart').innerHTML=`<svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">${grid}<path class="band" d="${band}"/><path class="curve" d="${path(prediction.x,prediction.mean)}"/>${reference?`<path class="truth-line" d="${path(reference.x,reference.y)}"/>`:''}${samples}<line class="axis" x1="${left}" x2="${width-right}" y1="${height-bottom}" y2="${height-bottom}"/><text class="axis-label" x="${width-right}" y="${height-1}" text-anchor="end">x</text><text class="axis-label" x="14" y="18">y</text></svg>`;
}
function renderComparison() {
 if (!bundle?.summary) return;
 const scenario=$('comparison-scenario').value, rows=bundle.summary.groups.filter(g=>g.scenario===scenario);
 $('comparison-rows').innerHTML=rows.map(g=>`<tr><td>${esc(namePolicy(g.policy))}</td><td>${esc(t(g.observation_model==='aware'?'aware':'identity'))}</td><td class="number">${g.n_seeds}</td><td class="number">${fmt(g.metrics.rmse_latent.mean)} ± ${fmt(g.metrics.rmse_latent.sd)}</td><td class="number">${percent(g.metrics.observation_95_coverage.mean)}</td><td class="number">${fmt(g.metrics.train_cost.mean,2)}</td><td class="number">${fmt(g.metrics.total_measurement_cost.mean,2)}</td><td class="number">${g.target_passes} / ${g.n_seeds}</td><td class="number">${g.assumption_stops} / ${g.n_seeds}</td></tr>`).join('');
 $('comparison-detail').textContent=`${bundle.summary.n_runs} runs · ${t('allSeeds')} ${t('counter')}`;
}
function renderAgenda() {
 const cards=lang==='ko'?[
 ['H1','관측 가능한 기전 차이를 질의한다','두 기전의 유한 후보와 관측 투영 정보이득을 구현했다. 후보 밖 정답에서도 시험한다.','partial'],
 ['H2','관측 연산자의 영향을 분리한다','동일 학습 질의에 aware/identity 연산자를 각각 적합한다. PINN/UDE 비교는 구현하지 않았다.','partial'],
 ['H3','합성값을 새 증거로 세지 않는다','출처·부모·분할 검사와 증거 혼입 거부를 구현했다. 생성 증강의 통계적 이득은 미검증이다.','runtimeOnly'],
 ['H4','공유 구조와 개체차를 구분한다','계층적 동역학과 실제 donor 일반화는 남아 있다. 현재 시드를 사람이나 동물 개체로 세지 않는다.','planned'],
 ['H5','저정밀 소스의 해로운 전이를 검사한다','공동 GP와 HF-only 전환을 비교한다. 전환은 오류를 놓칠 수 있으며 항상 유리하지 않다.','partial'],
 ['H6','적응적 수집 후 구간을 점검한다','구간 포함률·폭·NLL을 기록한다. Shift-aware conformal이나 온라인 보장으로 해석하지 않는다.','diagnosticOnly']
 ]:[
 ['H1','Query observable differences between mechanisms','Implemented a finite hypothesis library and observation-projected information gain, including out-of-library truth.','partial'],
 ['H2','Isolate the observation operator','Fit aware and identity operators on identical acquired measurements. PINN/UDE comparisons are not implemented.','partial'],
 ['H3','Do not count generated values as new evidence','Provenance, parent, and split checks reject evidence laundering. Statistical benefits of augmentation remain untested.','runtimeOnly'],
 ['H4','Separate shared structure and group variation','Hierarchical dynamics and real donor generalization remain future work. Seeds do not represent people or animals.','planned'],
 ['H5','Test harmful low-fidelity transfer','Compare a joint GP and HF-only fallback. The gate can miss harmful transfer and is not always beneficial.','partial'],
 ['H6','Check intervals after adaptive collection','Record coverage, width, and NLL. No shift-aware conformal or online guarantee is implemented.','diagnosticOnly']
 ];
 $('agenda-cards').innerHTML=cards.map(([id,title,body,status])=>`<article class="agenda-card"><p class="eyebrow">${id}</p><h3>${esc(title)}</h3><p>${esc(body)}</p><span class="badge ${status==='planned'?'warn':''}">${esc(t(status))}</span></article>`).join('');
}
function download(value, filename) { const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=filename;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),3000); }
$('lang-toggle').addEventListener('click',()=>{lang=lang==='ko'?'en':'ko';try{localStorage.setItem('closed-loop-language',lang);}catch(_){} labels();});
$('scenario').addEventListener('change',updateDesign);
$('load-record').addEventListener('click',loadBundled);
$('chart-readout').addEventListener('change',()=>current&&render());
$('show-truth').addEventListener('change',()=>current&&render());
$('comparison-scenario').addEventListener('change',renderComparison);
$('step-range').addEventListener('input',()=>{stopPlay();stepIndex=Number($('step-range').value);render();});
for (const [id,fn] of [['first-step',()=>0],['prev-step',()=>Math.max(0,stepIndex-1)],['next-step',()=>Math.min(current.snapshots.length-1,stepIndex+1)],['last-step',()=>current.snapshots.length-1]]) $(id).addEventListener('click',()=>{if(!current)return;stopPlay();stepIndex=fn();render();});
$('play').addEventListener('click',()=>{if(!current)return;if(timer){stopPlay();return;}if(stepIndex===current.snapshots.length-1)stepIndex=0;timer=setInterval(()=>{if(stepIndex>=current.snapshots.length-1){stopPlay();return;}stepIndex++;render();},850);render();});
$('export-run').addEventListener('click',()=>current&&download(current,`${current.run_id}.json`));
$('export-events').addEventListener('click',()=>current&&download({run_id:current.run_id,events:current.events},`${current.run_id}-events.json`));
$('import-json').addEventListener('change',async event=>{const file=event.target.files?.[0];if(!file)return;try{if(file.size>12*1024*1024)throw Error('size');setRun(JSON.parse(await file.text()),'import');message(t('loaded'));}catch(_){message(t('invalidFile'));}event.target.value='';});
$('run-new').addEventListener('click',async()=>{if(!csrfToken||busy)return;busy=true;updateMode();message(t('running'));try{const config={scenario:$('scenario').value,policy:$('policy').value,seed:Number($('seed').value),training_budget:Number($('budget').value),observation_model:$('observation-model').value};const response=await fetch('/api/run',{method:'POST',headers:{'Content-Type':'application/json','X-Lab-Token':csrfToken},body:JSON.stringify(config)});const data=await response.json();if(!response.ok||data.audit?.status!=='pass')throw Error(data.error||'audit failed');setRun(data.run,'live');message(t('finished'));}catch(_){message(t('runError'));}finally{busy=false;updateMode();}});
document.querySelectorAll('[data-tab]').forEach(button=>button.addEventListener('click',()=>{stopPlay();document.querySelectorAll('[data-tab]').forEach(b=>b.classList.toggle('active',b===button));document.querySelectorAll('.tab-panel').forEach(panel=>panel.hidden=panel.id!==button.dataset.tab);if(current&&button.dataset.tab==='experiment')render();}));
let resizeTimer;window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>current&&render(),100);});
labels();
if(bundle?.runs?.length){setRun(bundle.runs.find(r=>r.config.scenario==='mechanism_pair'&&r.config.policy==='guarded')||bundle.runs[0],'bundled');}else{message(lang==='ko'?'수록 데이터가 없다. Python suite 명령을 실행한다.':'No included data. Execute the Python suite command.');}
if((location.protocol==='http:'||location.protocol==='https:')&&['127.0.0.1','localhost'].includes(location.hostname))fetch('/api/health',{cache:'no-store'}).then(r=>r.ok?r.json():null).then(data=>{if(data?.mode==='synthetic-local-runner'){csrfToken=data.csrf_token;updateMode();}}).catch(()=>{});
})();
