from flask import Flask, render_template_string

app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kinetic Poetry Forest</title>
        <style>
            /* Base Styles */
            body, html {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                font-family: 'Georgia', serif;
                background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e);
                color: #fff;
            }

            /* Forest Container */
            #forest-container {
                position: relative;
                width: 100vw;
                height: 100vh;
                perspective: 1000px;
                overflow: hidden;
                cursor: pointer;
            }

            /* Header */
            .header {
                position: absolute;
                top: 20px;
                left: 20px;
                z-index: 10;
                opacity: 0.8;
                pointer-events: none;
            }

            .header h1 {
                margin: 0;
                font-size: 2rem;
                font-weight: 300;
                letter-spacing: 2px;
                text-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
            }

            .header p {
                margin: 5px 0 0;
                font-style: italic;
                font-size: 1rem;
            }

            /* Controls */
            .controls {
                position: absolute;
                bottom: 20px;
                right: 20px;
                z-index: 10;
            }

            button {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.4);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                cursor: pointer;
                font-family: inherit;
                transition: all 0.3s ease;
            }

            button:hover {
                background: rgba(255, 255, 255, 0.3);
            }

            /* Tree Styles */
            .tree {
                position: absolute;
                transform-style: preserve-3d;
                transform-origin: bottom center;
            }

            .trunk {
                position: absolute;
                bottom: 0;
                left: 50%;
                transform-origin: bottom center;
                background: linear-gradient(to right, #54350d, #8b5a2b, #54350d);
                transform: translateX(-50%) scaleY(0);
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
                border-radius: 3px;
                animation: growTrunk 2s forwards;
            }

            @keyframes growTrunk {
                to {
                    transform: translateX(-50%) scaleY(1);
                }
            }

            .branch {
                position: absolute;
                transform-origin: bottom center;
                background: linear-gradient(to right, #406428, #5a8d38, #406428);
                transform: scaleY(0);
                border-radius: 2px;
                animation: growBranch 1.5s forwards;
                animation-delay: var(--delay);
                box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
            }

            @keyframes growBranch {
                to {
                    transform: scaleY(1);
                }
            }

            .poetry-line {
                position: absolute;
                font-size: 0.9rem;
                color: #fff;
                text-shadow: 0 0 3px rgba(0, 0, 0, 0.7);
                opacity: 0;
                transform-origin: left center;
                transform: translateY(-50%) scale(0.5);
                animation: appearText 1s forwards;
                animation-delay: var(--delay);
                white-space: nowrap;
                pointer-events: none;
            }

            @keyframes appearText {
                to {
                    opacity: 1;
                    transform: translateY(-50%) scale(1);
                }
            }

            /* Leaf Style */
            .leaf {
                position: absolute;
                width: 10px;
                height: 10px;
                border-radius: 50% 0 50% 50%;
                background: radial-gradient(circle, rgba(154, 205, 50, 0.8) 0%, rgba(85, 107, 47, 0.8) 100%);
                transform: rotate(45deg) scale(0);
                animation: growLeaf 1s forwards;
                animation-delay: var(--delay);
                box-shadow: 0 0 3px rgba(0, 0, 0, 0.3);
            }

            @keyframes growLeaf {
                to {
                    transform: rotate(45deg) scale(1);
                }
            }

            /* Ground */
            .ground {
                position: absolute;
                bottom: 0;
                width: 100%;
                height: 5%;
                background: linear-gradient(to bottom, rgba(34, 49, 63, 0.8), rgba(22, 33, 41, 0.9));
                box-shadow: 0 -5px 15px rgba(0, 0, 0, 0.5);
                z-index: -1;
            }

            /* Stars */
            .star {
                position: absolute;
                width: 2px;
                height: 2px;
                background-color: white;
                border-radius: 50%;
                opacity: 0.7;
                animation: twinkle 3s infinite alternate;
            }

            @keyframes twinkle {
                0% {
                    opacity: 0.3;
                }
                100% {
                    opacity: 1;
                }
            }
        </style>
    </head>
    <body>
        <div id="forest-container">
            <div class="header">
                <h1>Kinetic Poetry Forest</h1>
                <p>Click anywhere to plant a poetry tree</p>
            </div>

            <div class="controls">
                <button id="clear-forest">Clear Forest</button>
            </div>

            <div class="ground"></div>
        </div>

        <script>
            document.addEventListener('DOMContentLoaded', () => {
                const forestContainer = document.getElementById('forest-container');
                const clearButton = document.getElementById('clear-forest');

                // Track trees to ensure unique poetry combinations
                let trees = [];
                let usedPoetryLines = new Set();

                // Create a starry background
                createStars();

                // Poetry collections arranged by themes
                const poetryLines = {
                    nature: [
                        "Leaves whisper secrets to the wind",
                        "Roots deep as time itself",
                        "Sunlight filters through emerald canopy",
                        "The forest breathes in silent rhythm",
                        "Branches reach for distant stars",
                        "Seasons change but trees remember",
                        "Ancient wisdom in rings of wood",
                        "Moss crawls slowly over stone",
                        "Dappled shadows dance on forest floor",
                        "Rain trickles down bark pathways"
                    ],
                    time: [
                        "Moments suspended like morning dew",
                        "Time unfolds in steady heartbeats",
                        "Yesterday's echoes in tomorrow's dawn",
                        "Eternity captured in a single breath",
                        "Memories linger like autumn leaves",
                        "Hours dissolve into timeless space",
                        "The present moment, a gift unwrapped",
                        "Seconds pass like gentle raindrops",
                        "Years grow rings around our souls",
                        "Dawn whispers promises of renewal"
                    ],
                    dreams: [
                        "Dreams take flight on midnight wings",
                        "Imagination blooms in darkness",
                        "Whispered hopes beneath starlight",
                        "The mind wanders untethered paths",
                        "Fantasy seeds planted in reality",
                        "Visions shimmer beyond horizon's edge",
                        "Slumber's journey through hidden realms",
                        "Possibilities unfold in dream gardens",
                        "Wishes dance with celestial light",
                        "Night reveals what daylight conceals"
                    ],
                    reflection: [
                        "Silence speaks volumes to listening hearts",
                        "Ripples of thought in still waters",
                        "The soul mirrors what eyes cannot see",
                        "Inner landscapes of forgotten truths",
                        "Echoes of self across dimensions",
                        "Questions bloom where answers fade",
                        "Wisdom grows in contemplation's soil",
                        "The heart's compass points ever homeward",
                        "Light reflects differently through tears",
                        "Self-discovery in fragments of wonder"
                    ]
                };

                // Convert the poetry object into a flat array for random selection
                const allPoetryLines = Object.values(poetryLines).flat();

                // Create stars for background
                function createStars() {
                    const stars = 150;
                    const container = document.getElementById('forest-container');

                    for (let i = 0; i < stars; i++) {
                        const star = document.createElement('div');
                        star.classList.add('star');

                        // Random position
                        star.style.left = `${Math.random() * 100}%`;
                        star.style.top = `${Math.random() * 70}%`; // Keep stars in upper portion

                        // Random size
                        const size = Math.random() * 2 + 1;
                        star.style.width = `${size}px`;
                        star.style.height = `${size}px`;

                        // Random twinkle timing
                        star.style.animationDuration = `${Math.random() * 3 + 2}s`;
                        star.style.animationDelay = `${Math.random() * 2}s`;

                        container.appendChild(star);
                    }
                }

                // Generate a unique set of poetry lines
                function getUniquePoetryLines(count) {
                    const result = [];
                    const availableLines = allPoetryLines.filter(line => !usedPoetryLines.has(line));

                    // If we're running out of unique lines, reset the used set
                    if (availableLines.length < count) {
                        usedPoetryLines.clear();
                        return getUniquePoetryLines(count);
                    }

                    // Select random lines from available ones
                    for (let i = 0; i < count; i++) {
                        const randomIndex = Math.floor(Math.random() * availableLines.length);
                        const line = availableLines[randomIndex];

                        result.push(line);
                        usedPoetryLines.add(line);
                        availableLines.splice(randomIndex, 1);
                    }

                    return result;
                }

                // Create a new tree at the clicked position
                function createTree(x, y) {
                    const tree = document.createElement('div');
                    tree.classList.add('tree');
                    tree.style.left = `${x}px`;
                    tree.style.bottom = '5%'; // Position above ground

                    // Create random tree properties
                    const treeHeight = Math.random() * 250 + 150; // 150-400px
                    const trunkWidth = Math.random() * 10 + 8; // 8-18px
                    const branchCount = Math.floor(Math.random() * 4) + 3; // 3-6 branches

                    // Create trunk
                    const trunk = document.createElement('div');
                    trunk.classList.add('trunk');
                    trunk.style.width = `${trunkWidth}px`;
                    trunk.style.height = `${treeHeight}px`;

                    tree.appendChild(trunk);

                    // Get unique poetry lines for this tree
                    const treePoetryLines = getUniquePoetryLines(branchCount);

                    // Add branches and poetry after a delay to allow trunk to grow first
                    setTimeout(() => {
                        createBranches(tree, branchCount, treeHeight, trunkWidth, treePoetryLines);
                    }, 500);

                    forestContainer.appendChild(tree);
                    trees.push(tree);

                    // Add subtle 3D rotation on mouseover
                    tree.addEventListener('mouseover', () => {
                        tree.style.transition = 'transform 2s ease';
                        tree.style.transform = `rotateY(${Math.random() * 10 - 5}deg) rotateX(${Math.random() * 5 - 2.5}deg)`;
                    });

                    tree.addEventListener('mouseout', () => {
                        tree.style.transition = 'transform 2s ease';
                        tree.style.transform = 'rotateY(0deg) rotateX(0deg)';
                    });
                }

                // Create branches for a tree
                function createBranches(tree, count, treeHeight, trunkWidth, poetryLines) {
                    const branchLengthRatio = 0.4; // Branch length as proportion of tree height
                    const branchWidthRatio = 0.7; // Branch width as proportion of trunk width

                    // Calculate minimum spacing between branches
                    const minSpacing = treeHeight * 0.15;
                    const maxStartHeight = treeHeight * 0.8; // Don't place branches at the very top
                    const minStartHeight = treeHeight * 0.2; // Don't place branches at the very bottom
                    const availableHeight = maxStartHeight - minStartHeight;

                    // Generate branch positions
                    const branchPositions = [];
                    for (let i = 0; i < count; i++) {
                        // Try to find a position that doesn't overlap with existing branches
                        let position;
                        let attempts = 0;
                        const maxAttempts = 10;

                        do {
                            position = Math.random() * availableHeight + minStartHeight;
                            attempts++;

                            // Check if this position is far enough from existing branches
                            const isTooClose = branchPositions.some(pos => Math.abs(pos - position) < minSpacing);

                            if (!isTooClose || attempts >= maxAttempts) break;
                        } while (true);

                        branchPositions.push(position);
                    }

                    // Sort positions from bottom to top
                    branchPositions.sort((a, b) => a - b);

                    // Create each branch with its poetry line
                    for (let i = 0; i < count; i++) {
                        const position = branchPositions[i];
                        const isLeftBranch = Math.random() < 0.5;
                        const angle = (isLeftBranch ? -1 : 1) * (Math.random() * 25 + 15); // 15-40 degrees
                        const branchLength = treeHeight * branchLengthRatio * (0.7 + Math.random() * 0.6); // Vary length
                        const branchWidth = trunkWidth * branchWidthRatio;

                        createBranch(
                            tree, 
                            position, 
                            angle, 
                            branchLength, 
                            branchWidth, 
                            isLeftBranch, 
                            poetryLines[i],
                            i
                        );
                    }
                }

                // Create an individual branch
                function createBranch(tree, position, angle, length, width, isLeftBranch, poetryLine, index) {
                    const branch = document.createElement('div');
                    branch.classList.add('branch');

                    // Position branch at the right height on the trunk
                    branch.style.bottom = `${position}px`;
                    branch.style.left = '50%';
                    branch.style.width = `${width}px`;
                    branch.style.height = `${length}px`;
                    branch.style.transformOrigin = 'bottom center';
                    branch.style.transform = `translateX(-50%) rotate(${angle}deg) scaleY(0)`;

                    // Add growth delay to create sequential growth
                    const growDelay = 1 + index * 0.3;
                    branch.style.setProperty('--delay', `${growDelay}s`);

                    // Add poetry text to the branch
                    setTimeout(() => {
                        const poetry = document.createElement('div');
                        poetry.classList.add('poetry-line');
                        poetry.textContent = poetryLine;

                        // Position the text along the branch
                        const textPosition = length * 0.6; // Position text at 60% of branch length

                        if (isLeftBranch) {
                            poetry.style.right = `${textPosition}px`;
                            poetry.style.transformOrigin = 'right center';
                            poetry.style.textAlign = 'right';
                        } else {
                            poetry.style.left = `${textPosition}px`;
                        }

                        poetry.style.top = '50%';

                        // Delay the appearance of text
                        const textDelay = growDelay + 0.5;
                        poetry.style.setProperty('--delay', `${textDelay}s`);

                        branch.appendChild(poetry);

                        // Add leaves to the branch
                        addLeaves(branch, length, width);
                    }, growDelay * 1000);

                    tree.appendChild(branch);
                }

                // Add leaves to a branch
                function addLeaves(branch, branchLength, branchWidth) {
                    const leafCount = Math.floor(branchLength / 15);

                    for (let i = 0; i < leafCount; i++) {
                        const leaf = document.createElement('div');
                        leaf.classList.add('leaf');

                        // Position leaves along the branch
                        const position = 50 + (branchLength - 50) * (i / leafCount);
                        const side = i % 2 === 0 ? -1 : 1; // Alternate sides

                        leaf.style.bottom = `${branchWidth / 2}px`;
                        leaf.style.left = `${position}px`;
                        leaf.style.transform = `translateY(${side * 5}px) rotate(${Math.random() * 90}deg) scale(0)`;

                        // Random size variations
                        const size = 8 + Math.random() * 7;
                        leaf.style.width = `${size}px`;
                        leaf.style.height = `${size}px`;

                        // Random shades of green
                        const hue = 90 + Math.floor(Math.random() * 40);
                        const saturation = 60 + Math.floor(Math.random() * 30);
                        const lightness = 30 + Math.floor(Math.random() * 30);
                        leaf.style.backgroundColor = `hsl(${hue}, ${saturation}%, ${lightness}%)`;

                        // Delay each leaf appearance
                        const delay = 1.5 + (i * 0.1);
                        leaf.style.setProperty('--delay', `${delay}s`);

                        branch.appendChild(leaf);
                    }
                }

                // Handle click event on the forest container
                forestContainer.addEventListener('click', (e) => {
                    // Don't create a tree if clicking on a button or control
                    if (e.target !== forestContainer && !e.target.classList.contains('ground')) {
                        return;
                    }

                    // Limit the number of trees to prevent performance issues
                    if (trees.length >= 10) {
                        alert('The forest is getting crowded! Clear some trees to plant more.');
                        return;
                    }

                    createTree(e.clientX, e.clientY);
                });

                // Clear the forest
                clearButton.addEventListener('click', () => {
                    trees.forEach(tree => tree.remove());
                    trees = [];
                    usedPoetryLines.clear();
                });

                // Optional: Create an initial tree for demonstration
                setTimeout(() => {
                    const initialX = window.innerWidth * 0.3;
                    const initialY = window.innerHeight * 0.5;
                    createTree(initialX, initialY);
                }, 1000);
            });
        </script>
    </body>
    </html>
    ''')


if __name__ == '__main__':
    app.run(debug=True, port=5000)