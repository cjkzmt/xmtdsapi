#重启命令
cd "C:\Users\A\AI\deepseek"
pm2 start dist/index.js --name "deepseek-free-api"
cd "C:\Users\A\AI\step"
pm2 start dist/index.js --name "step-free-api"
cd "C:\Users\A\AI\kimi"
pm2 start dist/index.js --name "kimi-free-api"
cd "C:\Users\A\AI\metaso"
pm2 start dist/index.js --name "metaso-free-api"
cd "C:\Users\A\AI\minimax"
pm2 start dist/index.js --name "minimax-free-api"
cd "C:\Users\A\AI\qwen"
pm2 start dist/index.js --name "qwen-free-api"
cd "C:\Users\A\AI\spark"
pm2 start dist/index.js --name "spark-free-api"

# 脚本权限
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser

Set-ExecutionPolicy Unrestricted
# AI安装名字
cd "C:\Users\A\AI\deepseek"
npm i
npm i -g pm2
npm run build
pm2 start dist/index.js --name "deepseek-free-api"
cd "C:\Users\A\AI\step"
npm i
npm i -g pm2
npm run build
pm2 start dist/index.js --name "step-free-api"
cd "C:\Users\A\AI\kimi"
npm i
npm i -g pm2
npm run build
pm2 start dist/index.js --name "kimi-free-api"

cd "C:\Users\A\AI\metaso"
npm i
npm i -g pm2
npm run build
pm2 start dist/index.js --name "metaso-free-api"

cd "C:\Users\A\AI\minimax"
npm i
npm i -g pm2
npm run build
pm2 start dist/index.js --name "minimax-free-api"
cd "C:\Users\A\AI\qwen"
npm i
npm i -g pm2
npm run build
pm2 start dist/index.js --name "qwen-free-api"
cd "C:\Users\A\AI\spark"
npm i
npm i -g pm2
npm run build
pm2 start dist/index.js --name "spark-free-api"

查看日志