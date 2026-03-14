
// Tab switching logic
function switchTab(tabId) {
    document.getElementById('tab-issue').classList.add('hidden');
    document.getElementById('tab-verify').classList.add('hidden');
    document.getElementById('tab-ledger').classList.add('hidden');
    
    document.getElementById('tab-' + tabId).classList.remove('hidden');
    if(tabId === 'ledger') fetchLedger();
}

// Generate Keypair
async function generateKeys() {
    try {
        const response = await fetch('/keys/generate');
        const data = await response.json();
        
        document.getElementById('keys-display').classList.remove('hidden');
        document.getElementById('gen-priv-key').value = data.private_key;
        document.getElementById('gen-pub-key').value = data.public_key;
        
        // Auto-fill the forms for convenience
        document.getElementById('issue-priv-key').value = data.private_key;
        document.getElementById('verify-pub-key').value = data.public_key;
        
    } catch (error) {
        alert("Failed to generate keys: " + error);
    }
}

// Issue Credential (University)
async function issueCredential() {
    const payload = {
        credential: {
            student_id: document.getElementById('issue-id').value,
            name: document.getElementById('issue-name').value,
            degree: document.getElementById('issue-degree').value,
            graduation_year: parseInt(document.getElementById('issue-year').value) || 0
        },
        private_key_pem: document.getElementById('issue-priv-key').value
    };

    document.getElementById('issue-result').innerText = "Processing cryptographics... Mining Block...";

    try {
        const response = await fetch('/issue', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        document.getElementById('issue-result').innerText = JSON.stringify(data, null, 2);
        
        if (data.signature) {
            // Auto-fill verify form for convenience
            document.getElementById('verify-id').value = payload.credential.student_id;
            document.getElementById('verify-name').value = payload.credential.name;
            document.getElementById('verify-degree').value = payload.credential.degree;
            document.getElementById('verify-year').value = payload.credential.graduation_year;
            document.getElementById('verify-sig').value = data.signature;
        }

    } catch (error) {
        document.getElementById('issue-result').innerText = "Error: " + error;
    }
}

// Verify Credential (Employer)
async function verifyCredential() {
    const payload = {
        credential: {
            student_id: document.getElementById('verify-id').value,
            name: document.getElementById('verify-name').value,
            degree: document.getElementById('verify-degree').value,
            graduation_year: parseInt(document.getElementById('verify-year').value) || 0
        },
        signature: document.getElementById('verify-sig').value,
        public_key_pem: document.getElementById('verify-pub-key').value
    };

    const iconEl = document.getElementById('verify-result-icon');
    const textEl = document.getElementById('verify-result-text');
    
    iconEl.innerText = "⏳";
    textEl.innerText = "Verifying ECDSA Signature & Blockchain State...";
    textEl.className = "text-lg font-medium text-gray-600";

    try {
        const response = await fetch('/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (data.valid) {
            iconEl.innerText = "✅";
            textEl.innerText = "AUTHENTIC: " + data.reason;
            textEl.className = "text-lg font-bold text-green-600";
        } else {
            iconEl.innerText = "❌";
            textEl.innerText = "FRAUD DETECTED: " + data.reason;
            textEl.className = "text-lg font-bold text-red-600";
        }

    } catch (error) {
        iconEl.innerText = "⚠️";
        textEl.innerText = "Network Error: " + error;
        textEl.className = "text-lg font-bold text-yellow-600";
    }
}

// Fetch and display Ledger
async function fetchLedger() {
    try {
        const response = await fetch('/chain');
        const data = await response.json();
        
        const statusEl = document.getElementById('ledger-status');
        if (data.is_valid) {
            statusEl.innerHTML = `<span class="text-green-600">✅ Blockchain is mathematically valid. Length: ${data.length} blocks.</span>`;
        } else {
            statusEl.innerHTML = `<span class="text-red-600">❌ CRITICAL: Blockchain integrity has been compromised!</span>`;
        }

        const blocksContainer = document.getElementById('ledger-blocks');
        blocksContainer.innerHTML = ''; // clear

        // Reverse to show newest blocks first
        const blocks = data.chain.reverse();
        
        blocks.forEach(block => {
            const blockEl = document.createElement('div');
            blockEl.className = "bg-gray-100 p-4 rounded border border-gray-300 font-mono text-xs overflow-x-auto";
            
            const isGenesis = block.index === 0;
            const badgeColor = isGenesis ? 'bg-blue-200 text-blue-800' : 'bg-purple-200 text-purple-800';
            
            blockEl.innerHTML = `
                <div class="mb-2 flex justify-between items-center">
                    <span class="font-bold text-sm">Block #${block.index}</span>
                    <span class="px-2 py-1 rounded text-xs font-bold ${badgeColor}">${isGenesis ? 'Genesis Block' : 'Credential Record'}</span>
                </div>
                <div><strong>Timestamp:</strong> ${new Date(block.timestamp * 1000).toLocaleString()}</div>
                <div><strong>Hash:</strong> <span class="text-purple-700">${block.hash}</span></div>
                <div><strong>Prev Hash:</strong> ${block.previous_hash}</div>
                <div><strong>Nonce:</strong> ${block.nonce}</div>
                <div class="mt-2 p-2 bg-gray-200 rounded">
                    <strong>Payload Data:</strong><br>
                    <pre>${JSON.stringify(block.data, null, 2)}</pre>
                </div>
            `;
            blocksContainer.appendChild(blockEl);
        });

    } catch (error) {
        document.getElementById('ledger-blocks').innerHTML = `<p class="text-red-500">Failed to fetch ledger: ${error}</p>`;
    }
}
