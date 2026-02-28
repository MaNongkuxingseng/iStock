#!/usr/bin/env python3
"""
简单Web服务器，替代mystock的web_service.py
提供基本的数据访问接口
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import socket
import sys
import time

class StockDataHandler(BaseHTTPRequestHandler):
    """处理股票数据请求"""
    
    def do_GET(self):
        """处理GET请求"""
        try:
            if self.path == '/health':
                self._send_json_response({'status': 'ok', 'service': 'simple-stock-api'})
                
            elif self.path == '/':
                self._send_json_response({
                    'service': 'Stock Data API',
                    'version': '1.0',
                    'endpoints': {
                        '/health': '健康检查',
                        '/instock/data': '获取股票数据',
                        '/instock/data?table_name=cn_stock_indicators_sell': '卖出指标数据'
                    }
                })
                
            elif self.path.startswith('/instock/data'):
                # 解析查询参数
                query_params = {}
                if '?' in self.path:
                    query_string = self.path.split('?')[1]
                    for param in query_string.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            query_params[key] = value
                
                # 根据参数返回数据
                table_name = query_params.get('table_name', '')
                date = query_params.get('date', '2026-02-27')
                
                if table_name == 'cn_stock_indicators_sell':
                    data = self._get_sell_indicators(date)
                else:
                    data = self._get_sample_data()
                
                self._send_json_response({'data': data, 'count': len(data)})
                
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _send_json_response(self, data):
        """发送JSON响应"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def _get_sell_indicators(self, date):
        """获取卖出指标数据"""
        return [
            {
                'code': '603949',
                'name': '雪龙集团',
                'date': date,
                'macd_golden_fork': 1,
                'kdj_golden_fork': 1,
                'rsi_overbought': 0,
                'volume_ratio': 0.78,
                'price_change_percent': -0.31
            },
            {
                'code': '002415',
                'name': '海康威视',
                'date': date,
                'macd_golden_fork': 1,
                'kdj_golden_fork': 0,
                'rsi_overbought': 0,
                'volume_ratio': 1.24,
                'price_change_percent': 0.56
            },
            {
                'code': '600519',
                'name': '贵州茅台',
                'date': date,
                'macd_golden_fork': 0,
                'kdj_golden_fork': 0,
                'rsi_overbought': 1,
                'volume_ratio': 0.92,
                'price_change_percent': -0.12
            }
        ]
    
    def _get_sample_data(self):
        """获取示例数据"""
        return self._get_sell_indicators('2026-02-27')
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        # 可以在这里添加日志记录逻辑
        pass

def check_port_available(port):
    """检查端口是否可用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', port))
        sock.close()
        return True
    except socket.error:
        return False

def main():
    """主函数"""
    port = 9988
    
    # 检查端口
    if not check_port_available(port):
        print(f"错误：端口 {port} 已被占用")
        sys.exit(1)
    
    # 启动服务器
    server = HTTPServer(('127.0.0.1', port), StockDataHandler)
    
    print("=" * 50)
    print(f"股票数据API服务器已启动")
    print(f"地址: http://127.0.0.1:{port}")
    print(f"健康检查: http://127.0.0.1:{port}/health")
    print(f"数据接口: http://127.0.0.1:{port}/instock/data")
    print("=" * 50)
    print("按 Ctrl+C 停止服务器")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器正在关闭...")
        server.server_close()
        print("服务器已关闭")

if __name__ == '__main__':
    main()