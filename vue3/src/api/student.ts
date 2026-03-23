
import request from '@/utils/request'

// 获取所有学生信息
export function getStudentInfo(): Promise<any> {
    return request({
        url: '/student/selectAll',
        method: 'get',
    })
}