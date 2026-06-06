const amountInp = document.getElementById('amount');
const amountVal = document.getElementById('amountValue');
const txCountInp = document.getElementById('txCount');
const txCountVal = document.getElementById('txCountValue');
const bitFeeEl = document.getElementById('bitFee');
const payboxFeeEl = document.getElementById('payboxFee');
const tonFeeEl = document.getElementById('tonFee');
const saveBitEl = document.getElementById('saveBit');
const savePayboxEl = document.getElementById('savePaybox');

function calc() {
    let amount = parseFloat(amountInp.value);
    let tx = parseInt(txCountInp.value);
    amountVal.textContent = amount;
    txCountVal.textContent = tx;
    let bit = amount * 0.015;
    let paybox = amount * 0.018 + 0.5;
    let ton = amount * 0.001;
    bitFeeEl.textContent = bit.toFixed(2);
    payboxFeeEl.textContent = paybox.toFixed(2);
    tonFeeEl.textContent = ton.toFixed(2);
    let saveB = Math.round((bit - ton) * tx * 12);
    let saveP = Math.round((paybox - ton) * tx * 12);
    saveBitEl.textContent = saveB.toLocaleString();
    savePayboxEl.textContent = saveP.toLocaleString();
}

amountInp.addEventListener('input', calc);
txCountInp.addEventListener('input', calc);
calc();
