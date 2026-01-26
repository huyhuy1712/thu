# 🚀 HƯỚNG DẪN DEPLOY LÊN RENDER - SIÊU ĐƠN GIẢN!

## 🎯 Tại sao chọn Render?
- ✅ **FREE tier** (không cần thẻ tín dụng)
- ✅ Deploy từ GitHub tự động
- ✅ Không cần biết SSH, Linux
- ✅ SSL/HTTPS miễn phí
- ✅ Auto restart khi crash
- ⚠️ Free tier sẽ sleep sau 15 phút không dùng (khởi động lại ~1 phút)

---

## 📋 Các bước deploy

### Bước 1: Push code lên GitHub

```powershell
# Mở PowerShell tại thư mục project
cd "d:\thực tập\thu"

# Nếu chưa có Git repository
git init
git add .
git commit -m "Initial commit for Render deployment"

# Tạo repo mới trên GitHub, sau đó:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

### Bước 2: Đăng ký Render

1. Vào https://render.com
2. Click **Sign Up**
3. Chọn **Sign up with GitHub** (dễ nhất)
4. Authorize Render truy cập GitHub

---

### Bước 3: Deploy từ GitHub

#### Cách 1: Dùng Blueprint (Tự động - Khuyên dùng)

1. Vào Dashboard Render
2. Click **New +** → **Blueprint**
3. Chọn repository của bạn
4. Render sẽ tự động đọc file `render.yaml` và tạo 2 services:
   - **teledeaf-api**: Web service (FastAPI) - có public URL
   - **teledeaf-grpc**: Background worker (gRPC)

#### Cách 2: Thủ công (nếu Blueprint không hoạt động)

**Tạo Web Service (API):**
1. Click **New +** → **Web Service**
2. Connect repository của bạn
3. Cấu hình:
   - **Name**: `teledeaf-api`
   - **Region**: Singapore (hoặc Oregon)
   - **Branch**: `main`
   - **Runtime**: Docker
   - **Docker Command**: `python -m app.api.api_main`
   - **Plan**: Free
4. Click **Create Web Service**

**Tạo Background Worker (gRPC - Optional):**
1. Click **New +** → **Background Worker**
2. Connect cùng repository
3. Cấu hình:
   - **Name**: `teledeaf-grpc`
   - **Region**: Singapore
   - **Branch**: `main`
   - **Runtime**: Docker
   - **Docker Command**: `python -m grpc_service.server.main`
   - **Plan**: Free
4. Click **Create Background Worker**

---

### Bước 4: Đợi deploy xong

1. Render sẽ:
   - ✅ Build Docker image (~5-10 phút lần đầu)
   - ✅ Deploy container
   - ✅ Tạo public URL (vd: `https://teledeaf-api.onrender.com`)

2. Theo dõi logs:
   - Click vào service
   - Tab **Logs** để xem quá trình build và run

---

### Bước 5: Test API

```bash
# Thay YOUR_APP_URL bằng URL Render cung cấp
curl https://teledeaf-api.onrender.com

# Test sign recognition endpoint
curl -X POST https://teledeaf-api.onrender.com/v3/api/sign-language/recognize \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "web",
    "language_code": "vn",
    "frames": ["..."],
    "previous_word": ""
  }'
```

---

## 🔄 Auto Deploy (CI/CD)

Render tự động deploy khi bạn push code:

```powershell
# Chỉnh sửa code
# ...

# Commit và push
git add .
git commit -m "Update feature X"
git push origin main

# Render tự động build và deploy! ✨
```

---

## ⚙️ Cấu hình nâng cao

### Thêm Environment Variables

1. Vào service dashboard
2. Tab **Environment**
3. Add biến môi trường nếu cần:
   ```
   GRPC_PORT=50051
   LOG_LEVEL=INFO
   ```

### Custom Domain (nếu có)

1. Tab **Settings**
2. Phần **Custom Domain**
3. Add domain của bạn (vd: `api.yourdomain.com`)
4. Cấu hình DNS theo hướng dẫn

---

## 📊 Monitoring

### Xem logs:
1. Vào service dashboard
2. Tab **Logs**

### Xem metrics:
1. Tab **Metrics** để xem:
   - CPU usage
   - Memory usage
   - Request count

---

## ⚠️ Giới hạn Free Tier

- **Memory**: 512MB (có thể không đủ cho AI model lớn)
- **CPU**: Shared
- **Sleep**: Sau 15 phút không request, service sẽ sleep
- **Build**: 500 build minutes/month
- **Bandwidth**: 100GB/month

### Nếu bị Out of Memory:

**Option 1: Upgrade lên Starter Plan ($7/tháng)**
- 2GB RAM
- Không sleep
- Dedicated CPU

**Option 2: Optimize model**
- Giảm kích thước model
- Dùng quantization

---

## 🐛 Troubleshooting

### Lỗi: Build failed

**Kiểm tra:**
```bash
# Test build local trước
docker build -t test .
docker run -p 8000:8000 test
```

### Lỗi: Out of Memory

**Giải pháp:**
1. Upgrade plan lên Starter ($7/month)
2. Hoặc chuyển sang Railway (RAM nhiều hơn trên free tier)
3. Hoặc deploy lên VPS

### Service sleep quá lâu

**Giải pháp:**
1. Dùng uptime monitoring (vd: UptimeRobot) ping mỗi 10 phút
2. Upgrade lên Starter plan (không sleep)

### Không kết nối được gRPC

Render free tier không support gRPC public. Giải pháp:
1. Chỉ dùng FastAPI REST API
2. Hoặc chạy gRPC + FastAPI trong cùng 1 container

---

## 🔄 Deploy cả 2 services trong 1 container

Nếu gRPC không hoạt động, chỉnh sửa để chạy cả 2:

**Tạo file `start_both.sh`:**
```bash
#!/bin/bash
# Start gRPC in background
python -m grpc_service.server.main &
# Start FastAPI in foreground
python -m app.api.api_main
```

**Update Dockerfile:**
```dockerfile
CMD ["bash", "start_both.sh"]
```

**Update `render.yaml`:**
```yaml
services:
  - type: web
    name: teledeaf-api
    env: docker
    dockerCommand: bash start_both.sh
```

---

## 📱 Sử dụng API

```javascript
// Từ frontend của bạn
const API_URL = 'https://teledeaf-api.onrender.com';

fetch(`${API_URL}/v3/api/sign-language/recognize`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    platform: 'web',
    language_code: 'vn',
    frames: [...],
    previous_word: ''
  })
});
```

---

## ✅ Checklist hoàn thành

- [ ] Push code lên GitHub
- [ ] Đăng ký Render với GitHub
- [ ] Deploy service từ repository
- [ ] Đợi build xong (5-10 phút)
- [ ] Test API với URL được cung cấp
- [ ] Setup auto-deploy (đã tự động)
- [ ] Monitor logs và metrics
- [ ] (Optional) Setup custom domain

---

## 💡 So sánh với các platform khác

| Platform | Free RAM | Sleep? | Deploy | Giá nâng cấp |
|----------|----------|--------|--------|--------------|
| **Render** | 512MB | Có (15 phút) | Dễ | $7/tháng |
| **Railway** | 512MB | Có | Rất dễ | $5/tháng |
| **Heroku** | 512MB | Có | Dễ | $7/tháng |
| **Google Cloud Run** | 1GB | Không | Trung bình | Pay-as-you-go |
| **VPS** | 2GB+ | Không | Khó | $5-6/tháng |

---

## 🆘 Cần trợ giúp?

**Render Docs**: https://render.com/docs

**Các lỗi thường gặp:**
- Build timeout → Giảm dependencies
- OOM (Out of Memory) → Upgrade plan hoặc optimize model
- Slow start → Do free tier sleep, upgrade để fix

---

**🎉 Xong! Bây giờ service của bạn đã online!**

URL của bạn sẽ có dạng: `https://teledeaf-api.onrender.com`
