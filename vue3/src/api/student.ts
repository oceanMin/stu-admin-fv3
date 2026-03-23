
import request from '@/utils/request'

// 获取所有学生信息
export function getStudentInfo(params?:any): Promise<any> {
    console.log('params:', params);
    return request({
        url: '/student/selectAll',
        method: 'get',
        params
    })
}