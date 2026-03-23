
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

// 新增学生信息
export function addStudentInfo(data:any): Promise<any> {
    return request({
        url: '/student/createStuInfo',
        method: 'post',
        data
    })
}

// 修改学生信息
export function updateStudentInfo(data:any): Promise<any> {
    return request({
        url: '/student/update',
        method: 'post',
        data
    })
}

// 删除学生信息
export function deleteStudentInfo(stu_id:string): Promise<any> {
    return request({
        url: `/student/delete/${stu_id}`,
        method: 'delete',
    })
}